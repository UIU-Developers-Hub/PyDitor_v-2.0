// src/components/Editor/EditorPane.tsx
import React from 'react';
import styled from 'styled-components';
import { EditorContent } from './EditorContent';
import { EditorToolbar } from './EditorToolbar';
import { EditorStatusBar } from './EditorStatusBar';

const EditorContainer = styled.div.attrs({
  className: 'flex flex-col h-full'
})``;

export const EditorPane: React.FC = () => {
  return (
    <EditorContainer>
      <EditorToolbar />
      <div className="flex-1">
        <EditorContent />
      </div>
      <EditorStatusBar />
    </EditorContainer>
  );
};