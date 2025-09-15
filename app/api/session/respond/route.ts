// API route to process user responses

import { NextRequest, NextResponse } from 'next/server';
import { SAWAService } from '@/lib/sawa-service';
import { SessionStore } from '@/lib/session-store';

export const runtime = 'nodejs';

export async function POST(request: NextRequest) {
  try {
    console.log('POST /api/session/respond - Starting...');

    const body = await request.json();
    console.log('Request body:', body);

    const { sessionId, response } = body;

    if (!sessionId || !response) {
      console.log('Missing required fields:', { sessionId: !!sessionId, response: !!response });
      return NextResponse.json(
        { error: 'Session ID and response are required' },
        { status: 400 }
      );
    }

    console.log('Loading session store...');
    const store = new SessionStore();

    console.log('Loading session:', sessionId);
    const session = await store.load(sessionId);

    if (!session) {
      console.log('Session not found:', sessionId);
      return NextResponse.json(
        { error: 'Session not found' },
        { status: 404 }
      );
    }

    console.log('Processing response with SAWA service...');
    const service = new SAWAService();
    const result = await service.processResponse(session, response);

    console.log('Saving session...');
    await store.save(result.session);

    console.log('Getting progress...');
    const progress = await service.getProgress(result.session);

    console.log('Response processing completed successfully');
    return NextResponse.json({
      evaluation: result.evaluation,
      nextQuestion: result.nextQuestion,
      currentFacet: result.session.currentFacet,
      completed: result.session.completed,
      progress,
    });
  } catch (error: any) {
    console.error('Failed to process response:', {
      message: error?.message,
      stack: error?.stack,
      name: error?.name
    });

    return NextResponse.json(
      {
        error: 'Failed to process response',
        details: process.env.NODE_ENV === 'development' ? error?.message : undefined
      },
      { status: 500 }
    );
  }
}