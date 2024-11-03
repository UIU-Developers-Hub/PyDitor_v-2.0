// File: src/App.tsx
// Directory: src/

import React from 'react';
import { FileSystemProvider } from './context/FileSystemContext';
import { ThemeProvider } from './context/theme/ThemeContext';
import Sidebar from './components/Sidebar';
import Editor from './components/Editor';

const App: React.FC = () => {
  return (
    <ThemeProvider>
      <FileSystemProvider>
        <div className="flex h-screen overflow-hidden bg-white dark:bg-gray-900">
          <div className="w-64 border-r border-gray-200 dark:border-gray-700">
            <Sidebar />
          </div>
          <div className="flex-1">
            <Editor />
          </div>
        </div>
      </FileSystemProvider>
    </ThemeProvider>
  );
};

export default App;