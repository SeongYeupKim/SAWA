// Types for SAWA system following GitHub structure

export type Facet = 'claim' | 'evidence' | 'reasoning' | 'backing' | 'qualifier' | 'rebuttal';

export interface SAWAMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
  facet: Facet;
  timestamp: string;
  evaluation?: FacetEvaluation;
}

export interface FacetEvaluation {
  level: 1 | 2 | 3 | 4;
  passed: boolean;
  feedback: string;
  suggestions: string[];
}

export interface SessionState {
  id: string;
  topic: string;
  createdAt: string;
  updatedAt: string;
  currentFacet: Facet;
  facets: Record<Facet, FacetState>;
  messages: SAWAMessage[];
  completed: boolean;
}

export interface FacetState {
  facet: Facet;
  completed: boolean;
  level: 1 | 2 | 3 | 4;
  attempts: number;
  bestResponse?: string;
  feedback?: string;
}

export interface RubricCriteria {
  facet: Facet;
  level: 1 | 2 | 3 | 4;
  description: string;
  examples: string[];
}