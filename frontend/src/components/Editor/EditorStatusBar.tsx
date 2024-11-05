// src/components/Editor/EditorStatusBar.tsx
import React from 'react';
import styled from 'styled-components';

const StatusBarContainer = styled.div.attrs({
  className: 'flex items-center px-2 h-6 text-sm'
})`
  background-color: ${props => props.theme.colors.background.statusBar}; // Using statusBar here
  color: ${props => props.theme.colors.foreground.secondary};
`;

export const EditorStatusBar: React.FC = () => {
  return (
    <StatusBarContainer>
      <span>Line 1, Column 1</span>
      <div className="flex-1" />
      <span>UTF-8</span>
    </StatusBarContainer>
  );
};
