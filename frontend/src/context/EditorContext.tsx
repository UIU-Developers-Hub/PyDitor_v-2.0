// src/context/EditorContext.tsx
import React, { createContext, useContext, useState, useCallback } from 'react';

interface EditorState {
  code: string;
  language: string;
  theme: 'vs-dark' | 'light';
  isConnected: boolean;
}

interface EditorContextType extends EditorState {
  updateCode: (code: string) => void;
  setLanguage: (language: string) => void;
  toggleTheme: () => void;
  saveCode: () => Promise<void>;
}

const defaultState: EditorState = {
  code: '',
  language: 'python',
  theme: 'vs-dark',
  isConnected: false
};

const EditorContext = createContext<EditorContextType | undefined>(undefined);

export const EditorProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, setState] = useState<EditorState>(defaultState);

  const updateCode = useCallback((code: string) => {
    setState(prev => ({ ...prev, code }));
  }, []);

  const setLanguage = useCallback((language: string) => {
    setState(prev => ({ ...prev, language }));
  }, []);

  const toggleTheme = useCallback(() => {
    setState(prev => ({
      ...prev,
      theme: prev.theme === 'vs-dark' ? 'light' : 'vs-dark'
    }));
  }, []);

  const saveCode = useCallback(async () => {
    try {
      const response = await fetch('http://localhost:8000/api/files/save', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content: state.code,
          language: state.language
        })
      });

      if (!response.ok) {
        throw new Error('Failed to save code');
      }
    } catch (error) {
      console.error('Error saving code:', error);
      throw error;
    }
  }, [state.code, state.language]);

  return (
    <EditorContext.Provider
      value={{
        ...state,
        updateCode,
        setLanguage,
        toggleTheme,
        saveCode
      }}
    >
      {children}
    </EditorContext.Provider>
  );
};

export const useEditor = () => {
  const context = useContext(EditorContext);
  if (context === undefined) {
    throw new Error('useEditor must be used within an EditorProvider');
  }
  return context;
};