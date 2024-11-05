// src/types/collaboration.ts
export interface Position {
    line: number;
    column: number;
  }
  
  export interface Cursor {
    userId: string;
    position: Position;
  }
  
  export interface CodeChange {
    userId: string;
    changes: Array<{
      range: {
        startLineNumber: number;
        startColumn: number;
        endLineNumber: number;
        endColumn: number;
      };
      text: string;
    }>;
  }
  
  export interface WebSocketMessage<T = unknown> {
    type: string;
    userId: string;
    data: T;
  }