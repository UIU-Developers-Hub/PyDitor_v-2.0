// File: src/hooks/useEditor.ts
// Directory: src/hooks/

import { useContext } from 'react';
import { FileSystemContext } from '../context/FileSystemContext';
import { fileService } from '../services/files';

interface UseFileSystemReturn {
  files: Array<{
    id: string;
    name: string;
    path: string;
    type: 'file' | 'folder';
    children?: Array<any>;
    isExpanded?: boolean;
  }>;
  selectedFile: string | null;
  loading: boolean;
  error: string | null;
  selectFile: (path: string) => void;
  toggleFolder: (path: string) => void;
  createFile: (parentPath: string, name: string) => Promise<void>;
  createFolder: (parentPath: string, name: string) => Promise<void>;
}

export const useFileSystem = (): UseFileSystemReturn => {
  const context = useContext(FileSystemContext);

  if (!context) {
    throw new Error('useFileSystem must be used within a FileSystemProvider');
  }

  const { state, dispatch } = context;

  const selectFile = (path: string) => {
    dispatch({ type: 'SELECT_FILE', payload: path });
  };

  const toggleFolder = (path: string) => {
    dispatch({ type: 'TOGGLE_FOLDER', payload: path });
  };

  const createFile = async (parentPath: string, name: string) => {
    try {
      dispatch({ type: 'SET_LOADING', payload: true });
      await fileService.createFile(parentPath, name);
      const files = await fileService.getFiles();
      dispatch({ type: 'SET_FILES', payload: files });
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: 'Failed to create file' });
      throw error;
    } finally {
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  };

  const createFolder = async (parentPath: string, name: string) => {
    try {
      dispatch({ type: 'SET_LOADING', payload: true });
      await fileService.createFolder(parentPath, name);
      const files = await fileService.getFiles();
      dispatch({ type: 'SET_FILES', payload: files });
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: 'Failed to create folder' });
      throw error;
    } finally {
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  };

  return {
    files: state.files,
    selectedFile: state.selectedFile,
    loading: state.loading,
    error: state.error,
    selectFile,
    toggleFolder,
    createFile,
    createFolder,
  };
};

export type FileSystemHook = ReturnType<typeof useFileSystem>;