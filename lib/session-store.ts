// Session storage management

import { SessionState } from './types';
import fs from 'fs/promises';
import path from 'path';

const STORAGE_DIR = path.join(process.cwd(), 'storage', 'sessions');

export class SessionStore {
  private storageReady: Promise<void>;

  constructor() {
    this.storageReady = this.ensureStorageDir();
  }

  private async ensureStorageDir(): Promise<void> {
    try {
      await fs.mkdir(STORAGE_DIR, { recursive: true });
      console.log('Storage directory ensured:', STORAGE_DIR);
    } catch (error) {
      console.error('Failed to create storage directory:', error);
      throw error;
    }
  }

  async save(session: SessionState): Promise<void> {
    await this.storageReady;
    const filePath = path.join(STORAGE_DIR, `${session.id}.json`);
    await fs.writeFile(filePath, JSON.stringify(session, null, 2));
  }

  async load(sessionId: string): Promise<SessionState | null> {
    try {
      await this.storageReady;
      const filePath = path.join(STORAGE_DIR, `${sessionId}.json`);
      const data = await fs.readFile(filePath, 'utf-8');
      return JSON.parse(data);
    } catch (error) {
      console.error('Failed to load session:', error);
      return null;
    }
  }

  async list(): Promise<string[]> {
    try {
      await this.storageReady;
      const files = await fs.readdir(STORAGE_DIR);
      return files
        .filter(f => f.endsWith('.json'))
        .map(f => f.replace('.json', ''));
    } catch (error) {
      console.error('Failed to list sessions:', error);
      return [];
    }
  }

  async delete(sessionId: string): Promise<void> {
    try {
      await this.storageReady;
      const filePath = path.join(STORAGE_DIR, `${sessionId}.json`);
      await fs.unlink(filePath);
    } catch (error) {
      console.error('Failed to delete session:', error);
    }
  }
}