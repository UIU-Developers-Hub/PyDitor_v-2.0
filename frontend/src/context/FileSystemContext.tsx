// File: src/context/FileSystemContext.tsx
// Directory: src/context/

import React, { createContext, useReducer, Dispatch } from 'react';
import type { FileSystemState, FileAction } from '../types/file';

interface FileSystemContextType {
  state: FileSystemState;
  dispatch: Dispatch<FileAction>;
}

const initialState: FileSystemState = {
  files: [],
  selectedFile: null,
  loading: false,
  error: null
};

export const FileSystemContext = createContext<FileSystemContextType | undefined>(undefined);

const fileSystemReducer = (state: FileSystemState, action: FileAction): FileSystemState => {
  switch (action.type) {
    case 'SET_FILES':
      return { ...state, files: action.payload };
    case 'SELECT_FILE':
      return { ...state, selectedFile: action.payload };
    case 'TOGGLE_FOLDER':
      return {
        ...state,
        files: state.files.map(file => 
          file.path === action.payload
            ? { ...file, isExpanded: !file.isExpanded }
            : file
        )
      };
    case 'SET_LOADING':
      return { ...state, loading: action.payload };
    case 'SET_ERROR':
      return { ...state, error: action.payload };
    default:
      return state;
  }
};

export const FileSystemProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(fileSystemReducer, initialState);

  return (
    <FileSystemContext.Provider value={{ state, dispatch }}>
      {children}
    </FileSystemContext.Provider>
  );
};