// src/components/FileOperations/FileActions.tsx

import React from 'react';

interface FileActionsProps {
  onCreateFile: (name: string, type: 'file' | 'directory') => void;
  onDeleteFile: (name: string) => void;
  onRenameFile: (oldName: string, newName: string) => void;
}

export const FileActions: React.FC<FileActionsProps> = ({ onCreateFile, onDeleteFile, onRenameFile }) => {
  const handleCreateFile = () => {
    const fileName = prompt("Enter new file name:");
    if (fileName) onCreateFile(fileName, 'file');
  };

  const handleCreateFolder = () => {
    const folderName = prompt("Enter new folder name:");
    if (folderName) onCreateFile(folderName, 'directory');
  };

  const handleDeleteFile = () => {
    const fileName = prompt("Enter the name of the file/folder to delete:");
    if (fileName) onDeleteFile(fileName);
  };

  const handleRenameFile = () => {
    const oldName = prompt("Enter the current name of the file/folder:");
    const newName = prompt("Enter the new name:");
    if (oldName && newName) onRenameFile(oldName, newName);
  };

  return (
    <div>
      <button onClick={handleCreateFile}>New File</button>
      <button onClick={handleCreateFolder}>New Folder</button>
      <button onClick={handleDeleteFile}>Delete</button>
      <button onClick={handleRenameFile}>Rename</button>
    </div>
  );
};
