// File: src/components/Editor/EditorPane.tsx
// Directory: src/components/Editor/

import React, { useState } from 'react';
import { useFileSystem } from '../../hooks/useEditor';
import MonacoEditor from '@monaco-editor/react';

const EditorPane: React.FC = () => {
  const { selectedFile, loading } = useFileSystem();
  const [content, setContent] = useState<string>('');
  const [theme] = useState<'light' | 'dark'>('light');

  const handleEditorChange = (value: string = '') => {
    setContent(value);
  };

  const getLanguage = (filename: string) => {
    const ext = filename?.split('.').pop() || '';
    const languageMap: Record<string, string> = {
      js: 'javascript',
      ts: 'typescript',
      jsx: 'javascript',
      tsx: 'typescript',
      py: 'python',
      html: 'html',
      css: 'css',
      json: 'json',
      md: 'markdown',
    };
    return languageMap[ext] || 'plaintext';
  };

  return (
    <div className="flex-1 h-full">
      {loading ? (
        <div className="flex items-center justify-center h-full">
          <span className="animate-spin">Loading...</span>
        </div>
      ) : selectedFile ? (
        <MonacoEditor
          height="100%"
          language={getLanguage(selectedFile)}
          theme={theme === 'dark' ? 'vs-dark' : 'light'}
          value={content}
          onChange={handleEditorChange}
          options={{
            minimap: { enabled: true },
            fontSize: 14,
            wordWrap: 'on',
            automaticLayout: true,
            lineNumbers: 'on',
            tabSize: 2,
          }}
        />
      ) : (
        <div className="flex items-center justify-center h-full text-gray-500">
          Select a file to edit
        </div>
      )}
    </div>
  );
};

export default EditorPane;