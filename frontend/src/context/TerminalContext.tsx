// src/context/TerminalContext.tsx
import React, { createContext, useContext, useState, useCallback } from 'react';

interface TerminalState {
  isVisible: boolean;
  isConnected: boolean;
  outputHistory: string[];
}

interface TerminalContextType extends TerminalState {
  toggleTerminal: () => void;
  clearTerminal: () => void;
  addOutput: (output: string) => void;
}

const TerminalContext = createContext<TerminalContextType | undefined>(undefined);

export const TerminalProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, setState] = useState<TerminalState>({
    isVisible: true,
    isConnected: false,
    outputHistory: [],
  });

  const toggleTerminal = useCallback(() => {
    setState(prev => ({ ...prev, isVisible: !prev.isVisible }));
  }, []);

  const clearTerminal = useCallback(() => {
    setState(prev => ({ ...prev, outputHistory: [] }));
  }, []);

  const addOutput = useCallback((output: string) => {
    setState(prev => ({
      ...prev,
      outputHistory: [...prev.outputHistory, output],
    }));
  }, []);

  return (
    <TerminalContext.Provider
      value={{
        ...state,
        toggleTerminal,
        clearTerminal,
        addOutput,
      }}
    >
      {children}
    </TerminalContext.Provider>
  );
};

export const useTerminal = () => {
  const context = useContext(TerminalContext);
  if (context === undefined) {
    throw new Error('useTerminal must be used within a TerminalProvider');
  }
  return context;
};