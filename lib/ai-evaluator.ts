// AI-powered evaluation system based on GitHub SAWA structure

import { Facet, FacetEvaluation } from './types';

// Dynamic imports to handle serverless environment
let Anthropic: any = null;
let OpenAI: any = null;

async function loadAIClients() {
  try {
    if (process.env.ANTHROPIC_API_KEY && !Anthropic) {
      const { Anthropic: AnthropicSDK } = await import('@anthropic-ai/sdk');
      Anthropic = AnthropicSDK;
    }
    if (process.env.OPENAI_API_KEY && !OpenAI) {
      const { default: OpenAISDK } = await import('openai');
      OpenAI = OpenAISDK;
    }
  } catch (error) {
    console.error('Error loading AI clients:', error);
  }
}

const FACET_PROMPTS: Record<Facet, string> = {
  claim: `Evaluate if this claim is:
    - Specific and contestable (not just a fact)
    - Contains conditional language (when, if, under certain conditions)
    - Testable with evidence
    - Shows complexity of thought`,

  evidence: `Evaluate if this evidence plan:
    - Specifies types of evidence needed
    - Mentions evaluation criteria (reliability, validity)
    - Shows understanding of evidence quality
    - Identifies specific sources or methods`,

  reasoning: `Evaluate if this reasoning:
    - Explains the logical connection (because, therefore)
    - States the general rule or principle
    - Specifies conditions for validity
    - Shows warrant clarity`,

  backing: `Evaluate if this backing:
    - References theories or prior research
    - Provides academic support
    - Shows domain knowledge
    - Connects to established principles`,

  qualifier: `Evaluate if this qualifier:
    - Acknowledges limitations
    - Uses appropriate hedging language
    - Identifies conditions and exceptions
    - Shows nuanced understanding`,

  rebuttal: `Evaluate if this rebuttal:
    - Presents strong counterarguments
    - Addresses opposition fairly
    - Provides response strategies
    - Shows critical thinking`
};

export class AIEvaluator {
  private anthropic?: any;
  private openai?: any;
  private initialized: boolean = false;

  constructor() {
    // Don't initialize in constructor for serverless compatibility
  }

  private async ensureInitialized() {
    if (this.initialized) return;

    try {
      await loadAIClients();

      if (process.env.ANTHROPIC_API_KEY && Anthropic) {
        this.anthropic = new Anthropic({
          apiKey: process.env.ANTHROPIC_API_KEY,
        });
        console.log('Anthropic client initialized');
      }

      if (process.env.OPENAI_API_KEY && OpenAI) {
        this.openai = new OpenAI({
          apiKey: process.env.OPENAI_API_KEY,
        });
        console.log('OpenAI client initialized');
      }

      if (!this.anthropic && !this.openai) {
        console.warn('No AI clients initialized - using fallback evaluation');
      }

      this.initialized = true;
    } catch (error) {
      console.error('Error initializing AI clients:', error);
      this.initialized = true; // Set to true to avoid retry loops
    }
  }

  async evaluateResponse(
    facet: Facet,
    response: string,
    topic: string
  ): Promise<FacetEvaluation> {
    await this.ensureInitialized();
    const prompt = `You are evaluating a student's response for the "${facet}" component of an argumentative essay about "${topic}".

${FACET_PROMPTS[facet]}

Student Response: "${response}"

Evaluate on a 1-4 scale:
1 = Underdeveloped: Missing key elements
2 = Developing: Basic understanding shown
3 = Proficient: Meets expectations
4 = Excellent: Sophisticated understanding

Provide:
1. A level (1-4)
2. Whether it passes (level >= 3)
3. Specific, actionable feedback
4. 2-3 suggestions for improvement

Response in JSON format:
{
  "level": number,
  "passed": boolean,
  "feedback": "specific feedback",
  "suggestions": ["suggestion1", "suggestion2", "suggestion3"]
}`;

    try {
      let result: string;

      if (this.anthropic) {
        console.log('Using Anthropic for evaluation');
        const message = await this.anthropic.messages.create({
          model: 'claude-3-haiku-20240307',
          max_tokens: 500,
          messages: [{ role: 'user', content: prompt }],
        });
        result = message.content[0].type === 'text' ? message.content[0].text : '';
      } else if (this.openai) {
        console.log('Using OpenAI for evaluation');
        const completion = await this.openai.chat.completions.create({
          model: 'gpt-4o-mini',
          messages: [{ role: 'user', content: prompt }],
          response_format: { type: 'json_object' },
          temperature: 0.3,
        });
        result = completion.choices[0]?.message?.content || '';
      } else {
        // Fallback to rule-based evaluation
        console.log('Using fallback evaluation');
        return this.fallbackEvaluation(facet, response);
      }

      if (!result) {
        throw new Error('Empty AI response');
      }

      const evaluation = JSON.parse(result);
      return {
        level: evaluation.level || 1,
        passed: evaluation.passed || false,
        feedback: evaluation.feedback || 'Please revise your response.',
        suggestions: evaluation.suggestions || ['Add more detail', 'Be more specific'],
      };
    } catch (error) {
      console.error('AI evaluation error:', error);
      console.log('Falling back to rule-based evaluation');
      return this.fallbackEvaluation(facet, response);
    }
  }

  private fallbackEvaluation(facet: Facet, response: string): FacetEvaluation {
    const length = response.length;
    const level = length > 100 ? 3 : length > 50 ? 2 : 1;

    return {
      level: level as 1 | 2 | 3 | 4,
      passed: level >= 3,
      feedback: level >= 3
        ? 'Good response. You can proceed to the next stage.'
        : 'Please provide more detail and specificity.',
      suggestions: [
        'Be more specific',
        'Add supporting details',
        'Consider edge cases'
      ],
    };
  }

  async generateSocraticQuestion(
    facet: Facet,
    previousResponse: string,
    feedback: string
  ): Promise<string> {
    await this.ensureInitialized();
    const prompt = `As a Socratic coach, generate a follow-up question for the "${facet}" stage.
Previous response: "${previousResponse}"
Feedback: "${feedback}"

Generate a thought-provoking question that guides deeper thinking without giving away the answer.`;

    try {
      if (this.anthropic) {
        const message = await this.anthropic.messages.create({
          model: 'claude-3-haiku-20240307',
          max_tokens: 150,
          messages: [{ role: 'user', content: prompt }],
        });
        return message.content[0].type === 'text' ? message.content[0].text : '';
      } else if (this.openai) {
        const completion = await this.openai.chat.completions.create({
          model: 'gpt-4o-mini',
          messages: [{ role: 'user', content: prompt }],
          temperature: 0.7,
        });
        return completion.choices[0]?.message?.content || '';
      }
    } catch (error) {
      console.error('Socratic question generation error:', error);
    }

    // Fallback questions
    const fallbackQuestions: Record<Facet, string> = {
      claim: 'Can you specify the conditions under which your claim holds true?',
      evidence: 'What specific evidence would best support your claim?',
      reasoning: 'How does your evidence logically connect to your claim?',
      backing: 'What established theories or research support your reasoning?',
      qualifier: 'What limitations or exceptions should we consider?',
      rebuttal: 'What counterarguments might critics raise?',
    };

    return fallbackQuestions[facet];
  }
}