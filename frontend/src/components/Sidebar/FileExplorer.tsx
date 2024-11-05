// src/components/FileExplorer/FileExplorer.tsx
import React from 'react';

interface FileExplorerProps {
  files: File[];
  onAddFile: (name: string, type: 'file' | 'directory') => void;
  onDeleteFile: (name: string) => void;
  onRenameFile: (oldName: string, newName: string) => void;
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
      <button aria-label="Delete File" onClick={() => onDeleteFile('FileName')}>
        Delete
      </button>
      <button aria-label="Rename File" onClick={() => onRenameFile('OldName', 'NewName')}>
        Rename
      </button>

      <ul>
        {files.map(file => (
          <li key={file.name}>
            {file.type === 'file' ? '📄' : '📁'} {file.name}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default FileExplorer;