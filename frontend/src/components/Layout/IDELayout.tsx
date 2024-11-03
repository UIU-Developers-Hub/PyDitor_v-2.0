// src/components/Layout/IDELayout.tsx
import React from 'react';
import CodeEditor from '../Editor/CodeEditor';
import TerminalComponent from '../Terminal/Terminal';
import { useTerminal } from '@/context/TerminalContext';
import { useEditor } from '@/context/EditorContext';

const IDELayout: React.FC = () => {
  const { isVisible, toggleTerminal } = useTerminal();
  const { code, updateCode, language, theme } = useEditor();

  return (
    <div className="h-screen flex flex-col bg-gray-900">
      <div className="flex-1 overflow-hidden">
        <CodeEditor
          code={code}
          language={language}
          theme={theme === 'vs-dark' ? 'dark' : 'light'}
          onChange={updateCode}
        />
      </div>
      {isVisible && (
        <div className="border-t border-gray-700">
          <TerminalComponent onClose={toggleTerminal} />
        </div>
      )}
    </div>
  );
};

export default IDELayout;