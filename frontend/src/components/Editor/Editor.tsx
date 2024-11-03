// File: src/components/Editor/Editor.tsx
// Directory: src/components/Editor/

import React from 'react';
import EditorToolbar from './EditorToolbar';
import EditorPane from './EditorPane';
import EditorStatusBar from './EditorStatusBar';

const Editor: React.FC = () => {
  return (
    <div className="flex flex-col h-full bg-white dark:bg-gray-900">
      <EditorToolbar />
      <div className="flex-1 overflow-hidden">
        <EditorPane />
      </div>
      <EditorStatusBar />
    </div>
  );
};

export default Editor;