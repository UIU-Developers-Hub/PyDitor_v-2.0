// src/components/Editor/MonacoEditor.tsx
import React, { useRef, useEffect } from 'react';
import * as monaco from 'monaco-editor';
import styled from 'styled-components';

const EditorContainer = styled.div`
  width: 100%;
  height: 100%;
  overflow: hidden;
`;

interface MonacoEditorProps {
  value: string;
  language: string;
  theme?: 'vs-dark' | 'light';
  onChange?: (value: string) => void;
}

export const MonacoEditor: React.FC<MonacoEditorProps> = ({
  value,
  language,
  theme = 'vs-dark',
  onChange
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const editorRef = useRef<monaco.editor.IStandaloneCodeEditor | null>(null);

  useEffect(() => {
    if (containerRef.current) {
      editorRef.current = monaco.editor.create(containerRef.current, {
        value,
        language,
        theme,
        minimap: { enabled: false },
        scrollBeyondLastLine: false,
        fontSize: 14,
        fontFamily: "'JetBrains Mono', monospace",
        automaticLayout: true
      });

      editorRef.current.onDidChangeModelContent(() => {
        onChange?.(editorRef.current?.getValue() || '');
      });

      // Configure editor settings
      monaco.editor.defineTheme('custom-dark', {
        base: 'vs-dark',
        inherit: true,
        rules: [],
        colors: {
          'editor.background': '#1e1e1e',
          'editor.foreground': '#d4d4d4',
          'editor.lineHighlightBackground': '#2f3139',
          'editor.selectionBackground': '#264f78',
          'editorCursor.foreground': '#d4d4d4',
        }
      });

      monaco.editor.setTheme('custom-dark');
    }

    return () => {
      editorRef.current?.dispose();
    };
  }, []);

  return <EditorContainer ref={containerRef} />;
};