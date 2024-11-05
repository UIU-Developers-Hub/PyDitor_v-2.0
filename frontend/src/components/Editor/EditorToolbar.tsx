// src/components/Editor/EditorToolbar.tsx
import React from 'react';
import styled from 'styled-components';
import { ActionButtons } from '../Toolbar/ActionButtons';

const ToolbarContainer = styled.div.attrs({
  className: 'flex items-center h-10 px-2 border-b'
})`
  background-color: ${props => props.theme.colors.background.secondary};
  border-color: ${props => props.theme.colors.border};
`;

export const EditorToolbar: React.FC = () => {
  return (
    <ToolbarContainer>
      <ActionButtons />
    </ToolbarContainer>
  );
};