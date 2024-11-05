import { FileNode } from '../types/file';

export const getFiles = async (): Promise<FileNode[]> => {
  const response = await fetch('/api/files');
  return response.json();
};

export const saveFile = async (file: FileNode): Promise<void> => {
  await fetch(`/api/files/${file.id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(file),
  });
};