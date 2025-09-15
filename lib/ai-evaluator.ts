// AI-powered evaluation system based on GitHub SAWA structure

import { Facet, FacetEvaluation } from './types';

// Import AI clients directly for better compatibility
let AnthropicClient: any = null;
let OpenAIClient: any = null;

// Load AI clients on first use
async function getAIClients() {
  if (!AnthropicClient && process.env.ANTHROPIC_API_KEY) {
    try {
      const { Anthropic } = await import('@anthropic-ai/sdk');
      AnthropicClient = new Anthropic({
        apiKey: process.env.ANTHROPIC_API_KEY,
      });
      console.log('Anthropic client initialized');
    } catch (error) {
      console.error('Failed to initialize Anthropic:', error);
    }
  }

  if (!OpenAIClient && process.env.OPENAI_API_KEY) {
    try {
      const { default: OpenAI } = await import('openai');
      OpenAIClient = new OpenAI({
        apiKey: process.env.OPENAI_API_KEY,
      });
      console.log('OpenAI client initialized');
    } catch (error) {
      console.error('Failed to initialize OpenAI:', error);
    }
  }

  return { anthropic: AnthropicClient, openai: OpenAIClient };
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
  constructor() {
    // Simple constructor for serverless compatibility
  }

  async evaluateResponse(
    facet: Facet,
    response: string,
    topic: string
  ): Promise<FacetEvaluation> {
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
      const { anthropic, openai } = await getAIClients();
      let result: string;

      if (anthropic) {
        console.log('Using Anthropic for evaluation');
        const message = await anthropic.messages.create({
          model: 'claude-3-haiku-20240307',
          max_tokens: 500,
          messages: [{ role: 'user', content: prompt }],
        });
        result = message.content[0].type === 'text' ? message.content[0].text : '';
      } else if (openai) {
        console.log('Using OpenAI for evaluation');
        const completion = await openai.chat.completions.create({
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
    const prompt = `As a Socratic coach, generate a follow-up question for the "${facet}" stage.
Previous response: "${previousResponse}"
Feedback: "${feedback}"

Generate a thought-provoking question that guides deeper thinking without giving away the answer.`;

    try {
      const { anthropic, openai } = await getAIClients();

      if (anthropic) {
        const message = await anthropic.messages.create({
          model: 'claude-3-haiku-20240307',
          max_tokens: 150,
          messages: [{ role: 'user', content: prompt }],
        });
        return message.content[0].type === 'text' ? message.content[0].text : '';
      } else if (openai) {
        const completion = await openai.chat.completions.create({
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