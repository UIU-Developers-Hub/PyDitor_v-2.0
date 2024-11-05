// src/components/FileOperations/FileTree.tsx

import React from 'react';
import styled from 'styled-components';
import { ChevronRight, File, Folder } from 'lucide-react';

const TreeContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
`;

const TreeItem = styled.div`
  display: flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.25rem;
  border-radius: 0.25rem;
  cursor: pointer;
  color: ${props => props.theme.colors.foreground.secondary};

  &:hover {
    background-color: ${props => props.theme.colors.accent};
    color: ${props => props.theme.colors.foreground.primary};
  }
`;

const IndentedTreeItem = styled(TreeItem)`
  margin-left: 1rem;
`;

// Export FileTree as a named export
export const FileTree: React.FC = () => {
  return (
    <TreeContainer>
      <TreeItem>
        <ChevronRight size={16} />
        <Folder size={16} />
        <span>src</span>
      </TreeItem>
      <IndentedTreeItem>
        <File size={16} />
        <span>index.tsx</span>
      </IndentedTreeItem>
    </TreeContainer>
  );
};
