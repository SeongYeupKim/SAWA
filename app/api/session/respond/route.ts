// API route to process user responses

import { NextRequest, NextResponse } from 'next/server';
import { SAWAService } from '@/lib/sawa-service';
import { SessionStore } from '@/lib/session-store';

export const runtime = 'nodejs';

export async function POST(request: NextRequest) {
  try {
    const { sessionId, response } = await request.json();

    if (!sessionId || !response) {
      return NextResponse.json(
        { error: 'Session ID and response are required' },
        { status: 400 }
      );
    }

    const store = new SessionStore();
    const session = await store.load(sessionId);

    if (!session) {
      return NextResponse.json(
        { error: 'Session not found' },
        { status: 404 }
      );
    }

    const service = new SAWAService();
    const result = await service.processResponse(session, response);

    await store.save(result.session);

    const progress = await service.getProgress(result.session);

    return NextResponse.json({
      evaluation: result.evaluation,
      nextQuestion: result.nextQuestion,
      currentFacet: result.session.currentFacet,
      completed: result.session.completed,
      progress,
    });
  } catch (error) {
    console.error('Failed to process response:', error);
    return NextResponse.json(
      { error: 'Failed to process response' },
      { status: 500 }
    );
  }
}