// File: src/components/Sidebar/FileExplorer.tsx
// Directory: src/components/Sidebar/

import React from 'react';
import { Plus } from 'lucide-react';
import { useFileSystem } from '../../hooks/useEditor';
import FileTree from './FileTree';

const FileExplorer: React.FC = () => {
  const { createFile, createFolder } = useFileSystem();

  const handleCreateFile = () => {
    const name = prompt('Enter file name:');
    if (name) createFile('/', name);
  };

  const handleCreateFolder = () => {
    const name = prompt('Enter folder name:');
    if (name) createFolder('/', name);
  };

  return (
    <div className="flex-1 flex flex-col overflow-hidden bg-gray-800 dark:bg-gray-900">
      <div className="flex items-center justify-between px-4 py-2 border-b border-gray-700">
        <h2 className="text-sm font-semibold text-white">Explorer</h2>
        <div className="flex gap-2">
          <button
            onClick={handleCreateFile}
            className="p-1 hover:bg-gray-700 rounded text-gray-300 hover:text-white"
            title="New File"
          >
            <Plus size={16} />
          </button>
          <button
            onClick={handleCreateFolder}
            className="p-1 hover:bg-gray-700 rounded text-gray-300 hover:text-white"
            title="New Folder"
          >
            <Plus size={16} />
          </button>
        </div>
      </div>
      <FileTree />
    </div>
  );
};

export default FileExplorer;