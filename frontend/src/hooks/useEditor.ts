// src/hooks/useEditor.ts
import { useCallback, useRef } from 'react';
import type { editor } from 'monaco-editor';

interface EditorHook {
  editorRef: React.MutableRefObject<{
    editor: editor.IStandaloneCodeEditor | null;
  }>;
  saveFile: () => void;
  runCode: () => void;
  formatCode: () => void;
  handleEditorDidMount: (editor: editor.IStandaloneCodeEditor) => void;
}

export const useEditor = (): EditorHook => {
  const editorRef = useRef<{ editor: editor.IStandaloneCodeEditor | null }>({
    editor: null
  });

  const handleEditorDidMount = useCallback((editor: editor.IStandaloneCodeEditor) => {
    editorRef.current.editor = editor;
  }, []);

  const saveFile = useCallback(() => {
    if (!editorRef.current.editor) return;
    const content = editorRef.current.editor.getValue();
    // Add save logic here
    console.log('Saving...', content);
  }, []);

  const runCode = useCallback(() => {
    if (!editorRef.current.editor) return;
    const content = editorRef.current.editor.getValue();
    // Add run logic here
    console.log('Running...', content);
  }, []);

  const formatCode = useCallback(() => {
    if (!editorRef.current.editor) return;
    editorRef.current.editor.getAction('editor.action.formatDocument')?.run();
  }, []);

  return {
    editorRef,
    saveFile,
    runCode,
    formatCode,
    handleEditorDidMount
  };
};