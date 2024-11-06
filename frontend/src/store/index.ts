// src/store/index.ts
import { configureStore } from '@reduxjs/toolkit';
import terminalReducer from './terminalSlice'; // Use correct name for the reducer

const store = configureStore({
  reducer: {
    terminal: terminalReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

export default store;
