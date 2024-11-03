// File: src/types/file.ts
// Directory: src/types/

export interface FileNode {
    id: string;
    name: string;
    path: string;
    type: 'file' | 'folder';
    content?: string;
    children?: FileNode[];
    isExpanded?: boolean;
    lastModified?: string;
    size?: number;
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