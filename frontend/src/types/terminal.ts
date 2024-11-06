// src/types/terminal.ts

export interface TerminalSession {
    id: string;
    output: string[]; // Array of strings for storing terminal output lines
    // Add any other session-specific properties as needed
  }
  
  export interface TerminalState {
    sessions: { [id: string]: TerminalSession }; // Map session ID to TerminalSession
    activeSessionId: string | null; // ID of the currently active terminal session
    isConnected: boolean; // WebSocket connection status
    error: string | null; // Error message if any issues arise
  }
  