// API route to export session as prep sheet

import { NextRequest, NextResponse } from 'next/server';
import { SAWAService } from '@/lib/sawa-service';
import { SessionStore } from '@/lib/session-store';

export const runtime = 'nodejs';

export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams;
    const sessionId = searchParams.get('sessionId');

    if (!sessionId) {
      return NextResponse.json(
        { error: 'Session ID is required' },
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
    const prepSheet = service.exportPrepSheet(session);

    return new NextResponse(prepSheet, {
      headers: {
        'Content-Type': 'text/markdown',
        'Content-Disposition': `attachment; filename="sawa-${sessionId}.md"`,
      },
    });
  } catch (error) {
    console.error('Failed to export session:', error);
    return NextResponse.json(
      { error: 'Failed to export session' },
      { status: 500 }
    );
  }
}