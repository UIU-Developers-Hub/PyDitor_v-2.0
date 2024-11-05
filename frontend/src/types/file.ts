// src/types/file.ts

export type FileLanguage = 'javascript' | 'typescript' | 'python' | 'html' | 'css' | 'json' | 'markdown' | 'yaml' | 'cpp' | 'java';

export interface FileNode {
  id: string;
  name: string;
  type: 'file' | 'directory'; // Use 'directory' instead of 'folder'
  content?: string;
  language?: FileLanguage;
  children?: FileNode[];
}

export interface FileSystemState {
  files: FileNode[];
  selectedFile: string | null;
  loading: boolean;
  error: string | null;
}

export type FileAction =
  | { type: 'SET_FILES'; payload: FileNode[] }
  | { type: 'SELECT_FILE'; payload: string }
  | { type: 'TOGGLE_FOLDER'; payload: string }
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_ERROR'; payload: string | null };
