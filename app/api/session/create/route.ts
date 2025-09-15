// API route to create a new SAWA session

import { NextRequest, NextResponse } from 'next/server';
import { SAWAService } from '@/lib/sawa-service';
import { SessionStore } from '@/lib/session-store';

// Ensure environment variables are loaded
if (!process.env.OPENAI_API_KEY && !process.env.ANTHROPIC_API_KEY) {
  console.warn('No AI API keys found. AI evaluation will use fallback mode.');
}

export const runtime = 'nodejs';

export async function POST(request: NextRequest) {
  try {
    console.log('Starting session creation...');

    const { topic } = await request.json();
    console.log('Received topic:', topic);

    if (!topic || typeof topic !== 'string') {
      return NextResponse.json(
        { error: 'Topic is required' },
        { status: 400 }
      );
    }

    console.log('Initializing SAWA service...');
    const service = new SAWAService();

    console.log('Initializing session store...');
    const store = new SessionStore();

    console.log('Creating session...');
    const session = await service.createSession(topic);

    console.log('Saving session...');
    await store.save(session);

    const firstQuestion = session.messages[session.messages.length - 1]?.content || "What is your main argument or claim about this topic? Be specific about the conditions under which it applies.";

    console.log('Session created successfully:', {
      sessionId: session.id,
      messagesCount: session.messages.length,
      firstQuestion
    });

    return NextResponse.json({
      sessionId: session.id,
      topic: session.topic,
      currentFacet: session.currentFacet,
      firstQuestion,
    });
  } catch (error: any) {
    console.error('Failed to create session:', {
      message: error?.message,
      stack: error?.stack,
      name: error?.name
    });

    return NextResponse.json(
      {
        error: 'Failed to create session',
        details: process.env.NODE_ENV === 'development' ? error?.message : undefined
      },
      { status: 500 }
    );
  }
}