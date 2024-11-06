// src/store/slices/terminalSlice.ts
import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface Session {
  content: string[];
  createdAt: string;
}

interface TerminalState {
  activeSessionId: string | null;
  sessions: Record<string, Session>;
}

const initialState: TerminalState = {
  activeSessionId: null,
  sessions: {},
};

const terminalSlice = createSlice({
  name: 'terminal',
  initialState,
  reducers: {
    setActiveSession: (state, action: PayloadAction<string>) => {
      state.activeSessionId = action.payload;
    },
    addSession: (state, action: PayloadAction<string>) => {
      const sessionId = action.payload;
      if (!state.sessions[sessionId]) {
        state.sessions[sessionId] = {
          content: [],
          createdAt: new Date().toISOString(),
        };
      }
    },
    removeSession: (state, action: PayloadAction<string>) => {
      const sessionId = action.payload;
      delete state.sessions[sessionId];
      if (state.activeSessionId === sessionId) {
        state.activeSessionId = null;
      }
    },
    updateSessionContent: (state, action: PayloadAction<{ id: string; content: string }>) => {
      const { id, content } = action.payload;
      if (state.sessions[id]) {
        state.sessions[id].content.push(content);
      }
    },
  },
});

export const {
  setActiveSession,
  addSession,
  removeSession,
  updateSessionContent,
} = terminalSlice.actions;

export default terminalSlice.reducer;
