// src/components/Sidebar/SidebarContainer.tsx
import React from 'react';
import { SidebarContainer as StyledSidebarContainer } from './styles';
import { FileExplorer } from '../FileExplorer/FileExplorer';
import { FileNode } from '../../types/file';

interface SidebarContainerProps {
  files: FileNode[];
  onAddFile: (name: string, type: 'file' | 'directory') => void;
  onDeleteFile: (id: string) => void;
  onRenameFile: (id: string, newName: string) => void;
}

// Change to named export
export const SidebarContainer: React.FC<SidebarContainerProps> = ({
  files,
  onAddFile,
  onDeleteFile,
  onRenameFile,
}) => {
  return (
    <StyledSidebarContainer>
      <FileExplorer
        files={files}
        onAddFile={onAddFile}
        onDeleteFile={onDeleteFile}
        onRenameFile={onRenameFile}
      />
    </StyledSidebarContainer>
  );
};
