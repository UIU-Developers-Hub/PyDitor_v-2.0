// src/components/FileOperations/FileExplorer.tsx
import React from 'react';
import styled from 'styled-components';
import { FileTree } from './FileTree';

const ExplorerContainer = styled.div.attrs({
  className: 'flex flex-col h-full'
})`
  background-color: ${props => props.theme.colors.background.secondary};
`;

export const FileExplorer: React.FC = () => {
  return (
    <ExplorerContainer>
      <div className="p-2">
        <FileTree />
      </div>
    </ExplorerContainer>
  );
};