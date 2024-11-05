// src/components/FileOperations/index.tsx
import React from 'react';
import styled from 'styled-components';
import { FileTree } from './FileTree';

const FileOperationsContainer = styled.div`
  height: 100%;
  background: ${props => props.theme.colors.sideBar}; // Access sideBar directly
  color: ${props => props.theme.colors.foreground.primary};
`;

export const FileOperations: React.FC = () => {
  return (
    <FileOperationsContainer>
      <FileTree />
    </FileOperationsContainer>
  );
};
