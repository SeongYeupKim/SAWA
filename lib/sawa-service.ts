// SAWA Service - Core logic following GitHub structure

import { AIEvaluator } from './ai-evaluator';
import { Facet, SessionState, SAWAMessage, FacetEvaluation } from './types';
import { v4 as uuidv4 } from 'uuid';

const FACET_SEQUENCE: Facet[] = ['claim', 'evidence', 'reasoning', 'backing', 'qualifier', 'rebuttal'];

const INITIAL_QUESTIONS: Record<Facet, string> = {
  claim: "What is your main argument or claim about this topic? Be specific about the conditions under which it applies.",
  evidence: "What evidence would you need to support your claim? Consider different types and their evaluation criteria.",
  reasoning: "How does your evidence connect to your claim? Explain the logical relationship.",
  backing: "What theories, principles, or prior research support your reasoning?",
  qualifier: "What are the limitations of your argument? When might it not apply?",
  rebuttal: "What counterarguments might others raise, and how would you respond?"
};

export class SAWAService {
  private evaluator: AIEvaluator;

  constructor() {
    this.evaluator = new AIEvaluator();
  }

  async createSession(topic: string): Promise<SessionState> {
    const now = new Date().toISOString();
    const id = uuidv4();

    const facets: SessionState['facets'] = {} as any;
    for (const facet of FACET_SEQUENCE) {
      facets[facet] = {
        facet,
        completed: false,
        level: 1,
        attempts: 0,
      };
    }

    const initialMessage: SAWAMessage = {
      role: 'system',
      content: `Let's develop a strong argumentative essay about: "${topic}". We'll work through six key components using the Toulmin model.`,
      facet: 'claim',
      timestamp: now,
    };

    const firstQuestion: SAWAMessage = {
      role: 'assistant',
      content: INITIAL_QUESTIONS.claim,
      facet: 'claim',
      timestamp: now,
    };

    return {
      id,
      topic,
      createdAt: now,
      updatedAt: now,
      currentFacet: 'claim',
      facets,
      messages: [initialMessage, firstQuestion],
      completed: false,
    };
  }

  async processResponse(
    session: SessionState,
    response: string
  ): Promise<{
    evaluation: FacetEvaluation;
    nextQuestion?: string;
    session: SessionState;
  }> {
    const currentFacet = session.currentFacet;

    // Add user response to messages
    session.messages.push({
      role: 'user',
      content: response,
      facet: currentFacet,
      timestamp: new Date().toISOString(),
    });

    // Evaluate response using AI
    const evaluation = await this.evaluator.evaluateResponse(
      currentFacet,
      response,
      session.topic
    );

    // Update facet state
    const facetState = session.facets[currentFacet];
    facetState.attempts++;
    facetState.level = evaluation.level;

    if (evaluation.passed) {
      facetState.completed = true;
      facetState.bestResponse = response;
      facetState.feedback = evaluation.feedback;
    }

    // Generate next question
    let nextQuestion: string | undefined;

    if (evaluation.passed) {
      // Move to next facet
      const currentIndex = FACET_SEQUENCE.indexOf(currentFacet);
      if (currentIndex < FACET_SEQUENCE.length - 1) {
        const nextFacet = FACET_SEQUENCE[currentIndex + 1];
        session.currentFacet = nextFacet;
        nextQuestion = INITIAL_QUESTIONS[nextFacet];

        // Add assistant message for next stage
        session.messages.push({
          role: 'assistant',
          content: `Great work on the ${currentFacet}! ${evaluation.feedback}\n\nNow let's move to the ${nextFacet} stage:\n${nextQuestion}`,
          facet: nextFacet,
          timestamp: new Date().toISOString(),
        });
      } else {
        // All stages completed
        session.completed = true;
        session.messages.push({
          role: 'assistant',
          content: `Excellent! You've completed all six components of your argument. ${evaluation.feedback}\n\nYour argumentative essay framework is now complete!`,
          facet: currentFacet,
          timestamp: new Date().toISOString(),
        });
      }
    } else {
      // Generate Socratic follow-up for current facet
      nextQuestion = await this.evaluator.generateSocraticQuestion(
        currentFacet,
        response,
        evaluation.feedback
      );

      // Add assistant message with feedback and follow-up
      session.messages.push({
        role: 'assistant',
        content: `${evaluation.feedback}\n\nLet me help you think deeper:\n${nextQuestion}`,
        facet: currentFacet,
        timestamp: new Date().toISOString(),
        evaluation,
      });
    }

    session.updatedAt = new Date().toISOString();

    return {
      evaluation,
      nextQuestion,
      session,
    };
  }

  async getProgress(session: SessionState): {
    completedStages: number;
    totalStages: number;
    currentStage: string;
    overallLevel: number;
  } {
    const completedStages = FACET_SEQUENCE.filter(f => session.facets[f].completed).length;
    const levels = FACET_SEQUENCE.map(f => session.facets[f].level);
    const overallLevel = Math.round(levels.reduce((a, b) => a + b, 0) / levels.length);

    return {
      completedStages,
      totalStages: FACET_SEQUENCE.length,
      currentStage: session.currentFacet,
      overallLevel: overallLevel as 1 | 2 | 3 | 4,
    };
  }

  exportPrepSheet(session: SessionState): string {
    const lines: string[] = [];
    lines.push(`# SAWA Argumentative Essay Framework`);
    lines.push(`## Topic: ${session.topic}`);
    lines.push(`## Date: ${new Date(session.createdAt).toLocaleDateString()}\n`);

    for (const facet of FACET_SEQUENCE) {
      const state = session.facets[facet];
      const title = facet.charAt(0).toUpperCase() + facet.slice(1);

      lines.push(`### ${title}`);
      if (state.bestResponse) {
        lines.push(`**Response:** ${state.bestResponse}`);
        lines.push(`**Level:** ${state.level}/4`);
        if (state.feedback) {
          lines.push(`**Feedback:** ${state.feedback}`);
        }
      } else {
        lines.push(`*Not completed*`);
      }
      lines.push('');
    }

    return lines.join('\n');
  }
}