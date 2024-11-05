// src/components/Editor/CollaborativeEditor.tsx
import React, { useEffect, useRef } from 'react';
import { Editor } from '@monaco-editor/react';
import { useCollaboration } from '../../context/CollaborationContext';
import { useFileSystem } from '../../context/FileSystemContext';

export const CollaborativeEditor: React.FC = () => {
  const editorRef = useRef<any>(null);
  const { selectedFile, updateFile } = useFileSystem();
  const { cursors, sendCursorPosition, sendCodeChange } = useCollaboration();

  useEffect(() => {
    if (!editorRef.current) return;

    const decorations = Array.from(cursors.values()).map(cursor => ({
      range: {
        startLineNumber: cursor.position.line,
        startColumn: cursor.position.column,
        endLineNumber: cursor.position.line,
        endColumn: cursor.position.column + 1
      },
      options: {
        className: 'cursor-decoration',
        hoverMessage: { value: `${cursor.userId}'s cursor` }
      }
    }));

    editorRef.current.deltaDecorations([], decorations);
  }, [cursors]);

  const handleEditorDidMount = (editor: any) => {
    editorRef.current = editor;

    editor.onDidChangeCursorPosition(({ position }: any) => {
      sendCursorPosition({
        line: position.lineNumber,
        column: position.column
      });
    });

    editor.onDidChangeModelContent((event: any) => {
      sendCodeChange(event.changes);
      if (selectedFile) {
        updateFile(selectedFile.id, editor.getValue());
      }
    });
  };

  return (
    <div className="h-full">
      <Editor
        height="100%"
        defaultLanguage="javascript"
        theme="vs-dark"
        value={selectedFile?.content || ''}
        onMount={handleEditorDidMount}
        options={{
          minimap: { enabled: true },
          scrollBeyondLastLine: false,
          fontSize: 14,
          automaticLayout: true
        }}
      />
    </div>
  );
};