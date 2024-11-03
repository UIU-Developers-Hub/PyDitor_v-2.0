// File: src/utils/format.ts
// Directory: src/utils/

import { type ClassValue as CVType, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: CVType[]) {
  return twMerge(clsx(inputs));
}

export function formatFileSize(size: number): string {
  const units = ['B', 'KB', 'MB', 'GB', 'TB'];
  let index = 0;
  let fileSize = size;

  while (fileSize >= 1024 && index < units.length - 1) {
    fileSize /= 1024;
    index++;
  }

  return `${fileSize.toFixed(1)} ${units[index]}`;
}

export function getFileIcon(filename: string): string {
  const ext = filename.split('.').pop()?.toLowerCase() || '';
  // Add more file type mappings as needed
  const iconMap: Record<string, string> = {
    ts: 'typescript',
    tsx: 'react',
    js: 'javascript',
    jsx: 'react',
    json: 'json',
    html: 'html',
    css: 'css',
    scss: 'sass',
    md: 'markdown',
    py: 'python',
  };

  return iconMap[ext] || 'file';
}