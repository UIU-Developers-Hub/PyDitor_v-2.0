// src/hooks/useKeyboardShortcuts.ts
import { useEffect, useCallback } from 'react';
import { editor as monacoEditor } from 'monaco-editor';

export const useKeyboardShortcuts = (editor: monacoEditor.IStandaloneCodeEditor | null) => {
  const handleKeyPress = useCallback((e: KeyboardEvent) => {
    if (!editor) return;

    // Ctrl/Cmd + S to save
    if ((e.ctrlKey || e.metaKey) && e.key === 's') {
      e.preventDefault();
      const content = editor.getValue();
      // Implement save logic
      console.log('Saving...', content);
    }

    // Ctrl/Cmd + F to format
    if ((e.ctrlKey || e.metaKey) && e.key === 'f') {
      e.preventDefault();
      editor.getAction('editor.action.formatDocument')?.run();
    }
  }, [editor]);

  useEffect(() => {
    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, [handleKeyPress]);
};