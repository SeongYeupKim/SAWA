// Session storage management - Serverless compatible

import { SessionState } from './types';

// In-memory storage for serverless environments
const sessionCache = new Map<string, SessionState>();

// Simple file system wrapper that works in serverless
const isServerless = process.env.VERCEL || process.env.AWS_LAMBDA_FUNCTION_NAME;

async function ensureStorageDir() {
  if (isServerless) return; // Skip for serverless

  try {
    const fs = await import('fs/promises');
    const path = await import('path');
    const STORAGE_DIR = path.join(process.cwd(), 'storage', 'sessions');
    await fs.mkdir(STORAGE_DIR, { recursive: true });
  } catch (error) {
    console.warn('File system not available, using memory storage');
  }
}

export class SessionStore {
  private storageReady: Promise<void>;

  constructor() {
    this.storageReady = ensureStorageDir();
  }

  async save(session: SessionState): Promise<void> {
    if (isServerless) {
      // Use in-memory storage for serverless
      sessionCache.set(session.id, { ...session });
      console.log('Session saved to memory:', session.id);
      return;
    }

    try {
      await this.storageReady;
      const fs = await import('fs/promises');
      const path = await import('path');
      const STORAGE_DIR = path.join(process.cwd(), 'storage', 'sessions');
      const filePath = path.join(STORAGE_DIR, `${session.id}.json`);
      await fs.writeFile(filePath, JSON.stringify(session, null, 2));
      console.log('Session saved to file:', session.id);
    } catch (error) {
      console.warn('File save failed, using memory fallback:', error);
      sessionCache.set(session.id, { ...session });
    }
  }

  async load(sessionId: string): Promise<SessionState | null> {
    // Try memory first (works in all environments)
    if (sessionCache.has(sessionId)) {
      console.log('Session loaded from memory:', sessionId);
      return { ...sessionCache.get(sessionId)! };
    }

    if (isServerless) {
      console.log('Session not found in memory:', sessionId);
      return null;
    }

    try {
      await this.storageReady;
      const fs = await import('fs/promises');
      const path = await import('path');
      const STORAGE_DIR = path.join(process.cwd(), 'storage', 'sessions');
      const filePath = path.join(STORAGE_DIR, `${sessionId}.json`);
      const data = await fs.readFile(filePath, 'utf-8');
      const session = JSON.parse(data);
      // Cache it for future use
      sessionCache.set(sessionId, { ...session });
      console.log('Session loaded from file:', sessionId);
      return session;
    } catch (error) {
      console.error('Failed to load session:', error);
      return null;
    }
  }

  async list(): Promise<string[]> {
    const memoryKeys = Array.from(sessionCache.keys());

    if (isServerless) {
      return memoryKeys;
    }

    try {
      await this.storageReady;
      const fs = await import('fs/promises');
      const path = await import('path');
      const STORAGE_DIR = path.join(process.cwd(), 'storage', 'sessions');
      const files = await fs.readdir(STORAGE_DIR);
      const fileKeys = files
        .filter(f => f.endsWith('.json'))
        .map(f => f.replace('.json', ''));

      // Combine memory and file keys
      return Array.from(new Set([...memoryKeys, ...fileKeys]));
    } catch (error) {
      console.error('Failed to list sessions:', error);
      return memoryKeys;
    }
  }

  async delete(sessionId: string): Promise<void> {
    sessionCache.delete(sessionId);

    if (!isServerless) {
      try {
        await this.storageReady;
        const fs = await import('fs/promises');
        const path = await import('path');
        const STORAGE_DIR = path.join(process.cwd(), 'storage', 'sessions');
        const filePath = path.join(STORAGE_DIR, `${sessionId}.json`);
        await fs.unlink(filePath);
      } catch (error) {
        console.error('Failed to delete session file:', error);
      }
    }
  }
}