// src/components/Editor/EditorContent.tsx
import React from 'react';
import styled from 'styled-components';
import { Editor } from '@monaco-editor/react';

const EditorContainer = styled.div`
  height: 100%;
  overflow: hidden;
`;

export const EditorContent: React.FC = () => {
  return (
    <EditorContainer>
      <Editor
        height="100%"
        defaultLanguage="typescript"
        theme="vs-dark"
        options={{
          fontFamily: 'JetBrains Mono',
          fontSize: 14,
          minimap: { enabled: false }
        }}
      />
    </EditorContainer>
  );
};