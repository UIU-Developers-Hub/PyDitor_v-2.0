// src/components/Editor/index.tsx

import React from 'react';
import { EditorPaneContainer, LineNumber, CodeArea } from './styles';

const EditorPane: React.FC = () => {
  return (
    <EditorPaneContainer>
      <LineNumber>1</LineNumber>
      <CodeArea>
        // Your code goes here
      </CodeArea>
    </EditorPaneContainer>
  );
};

export default EditorPane;
