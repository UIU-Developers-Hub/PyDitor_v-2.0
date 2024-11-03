// File: src/components/Editor/EditorStatusBar.tsx
// Directory: src/components/Editor/

import React from 'react';
import { useFileSystem } from '../../hooks/useEditor';

const EditorStatusBar: React.FC = () => {
  const { selectedFile } = useFileSystem();

  const getFileInfo = () => {
    if (!selectedFile) return null;
    const parts = selectedFile.split('.');
    const extension = parts[parts.length - 1];
    return {
      language: extension.toUpperCase(),
      encoding: 'UTF-8',
      lineEnding: 'LF',
    };
  };

  const fileInfo = getFileInfo();

  return (
    <div className="h-6 flex items-center justify-between px-4 bg-gray-800 dark:bg-gray-900 text-xs text-gray-300 border-t border-gray-700">
      <div className="flex items-center space-x-4">
        {fileInfo && (
          <>
            <span>{fileInfo.language}</span>
            <span>{fileInfo.encoding}</span>
            <span>{fileInfo.lineEnding}</span>
          </>
        )}
      </div>
      <div className="flex items-center space-x-4">
        <span>Ln 1, Col 1</span>
        <span>Spaces: 2</span>
      </div>
    </div>
  );
};

export default EditorStatusBar;