// src/main.tsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import '@fontsource/jetbrains-mono';
import '@fontsource/fira-code';
import './styles/global.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);