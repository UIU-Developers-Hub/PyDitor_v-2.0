// src/context/CollaborationContext.tsx
import React, { createContext, useContext, useEffect, useState } from 'react';
import { WebSocketService } from '../services/websocket';
import { Cursor, CodeChange, WebSocketMessage, Position } from '../types/collaboration';

interface CollaborationContextType {
  cursors: Map<string, Cursor>;
  sendCursorPosition: (position: Position) => void;
  sendCodeChange: (change: CodeChange) => void;
}

const CollaborationContext = createContext<CollaborationContextType | null>(null);

export const CollaborationProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [ws] = useState(() => new WebSocketService('ws://localhost:8000/ws'));
  const [cursors, setCursors] = useState<Map<string, Cursor>>(new Map());

  useEffect(() => {
    ws.connect();

    ws.subscribe('cursor', (data: unknown) => {
      const message = data as WebSocketMessage<Cursor>;
      if (message?.userId && message?.data?.position) {
        setCursors(prev => {
          const next = new Map(prev);
          next.set(message.userId, message.data);
          return next;
        });
      }
    });

    ws.subscribe('codeChange', (data: unknown) => {
      const message = data as WebSocketMessage<CodeChange>;
      if (message?.data?.changes) {
        // Handle code changes
        console.log('Code change:', message.data);
      }
    });

    return () => ws.disconnect();
  }, []);

  const sendCursorPosition = (position: Position) => {
    ws.send('cursor', { position });
  };

  const sendCodeChange = (change: CodeChange) => {
    ws.send('codeChange', { change });
  };

  return (
    <CollaborationContext.Provider value={{ cursors, sendCursorPosition, sendCodeChange }}>
      {children}
    </CollaborationContext.Provider>
  );
};

export const useCollaboration = () => {
  const context = useContext(CollaborationContext);
  if (!context) {
    throw new Error('useCollaboration must be used within a CollaborationProvider');
  }
  return context;
};