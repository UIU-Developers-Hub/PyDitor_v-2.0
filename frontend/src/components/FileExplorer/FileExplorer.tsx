// src/components/FileExplorer/FileExplorer.tsx
import React from 'react';
import { FileNode } from '../../types/file';

interface FileExplorerProps {
  files: FileNode[];
  onAddFile: (name: string, type: 'file' | 'directory') => void;
  onDeleteFile: (id: string) => void;
  onRenameFile: (id: string, newName: string) => void;
}

export const FileExplorer: React.FC<FileExplorerProps> = ({
  files,
  onAddFile,
  onDeleteFile,
  onRenameFile,
}) => {
  return (
    <div>
      <button aria-label="Add New File" onClick={() => onAddFile('NewFile', 'file')}>
        New File
      </button>
      <button aria-label="Add New Folder" onClick={() => onAddFile('NewFolder', 'directory')}>
        New Folder
      </button>
      <button aria-label="Delete File" onClick={() => onDeleteFile('FileID')}>
        Delete
      </button>
      <button aria-label="Rename File" onClick={() => onRenameFile('OldID', 'NewName')}>
        Rename
      </button>

      <ul>
        {files.map(file => (
          <li key={file.id}>
            {file.type === 'file' ? '📄' : '📁'} {file.name}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default FileExplorer;
