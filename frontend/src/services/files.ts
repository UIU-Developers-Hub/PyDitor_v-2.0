// File: src/services/files.ts
// Directory: src/services/

import { FileNode } from '@/types/file';

class FileService {
  private baseUrl = '/api/files';

  async getFiles(): Promise<FileNode[]> {
    const response = await fetch(`${this.baseUrl}/tree`);
    if (!response.ok) throw new Error('Failed to fetch files');
    return response.json();
  }

  async createFile(parentPath: string, name: string): Promise<FileNode> {
    const response = await fetch(this.baseUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name,
        path: `${parentPath}/${name}`,
        type: 'file',
        content: ''
      })
    });
    if (!response.ok) throw new Error('Failed to create file');
    return response.json();
  }

  async createFolder(parentPath: string, name: string): Promise<FileNode> {
    const response = await fetch(this.baseUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name,
        path: `${parentPath}/${name}`,
        type: 'folder'
      })
    });
    if (!response.ok) throw new Error('Failed to create folder');
    return response.json();
  }

  async deleteNode(path: string): Promise<void> {
    const response = await fetch(`${this.baseUrl}${path}`, {
      method: 'DELETE'
    });
    if (!response.ok) throw new Error('Failed to delete node');
  }

  async renameNode(oldPath: string, newPath: string): Promise<FileNode> {
    const response = await fetch(`${this.baseUrl}${oldPath}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ newPath })
    });
    if (!response.ok) throw new Error('Failed to rename node');
    return response.json();
  }
}

export const fileService = new FileService();