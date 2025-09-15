// API route to create a new SAWA session

import { NextRequest, NextResponse } from 'next/server';
import { SAWAService } from '@/lib/sawa-service';
import { SessionStore } from '@/lib/session-store';

export const runtime = 'nodejs';

export async function POST(request: NextRequest) {
  try {
    const { topic } = await request.json();

    if (!topic || typeof topic !== 'string') {
      return NextResponse.json(
        { error: 'Topic is required' },
        { status: 400 }
      );
    }

    const service = new SAWAService();
    const store = new SessionStore();

    const session = await service.createSession(topic);
    await store.save(session);

    const firstQuestion = session.messages[session.messages.length - 1]?.content || "What is your main argument or claim about this topic? Be specific about the conditions under which it applies.";

    console.log('Session created:', {
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
  } catch (error) {
    console.error('Failed to create session:', error);
    return NextResponse.json(
      { error: 'Failed to create session' },
      { status: 500 }
    );
  }
}