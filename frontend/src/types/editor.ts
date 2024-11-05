// src/types/editor.ts
export interface EditorContentProps {
  className?: string;
}

export interface EditorPaneProps {
  className?: string;
}

export interface EditorStatusBarProps {
  className?: string;
}

export interface EditorToolbarProps {
  onSave: () => void;
  onRun: () => void;
  onFormat: () => void;
  onFullscreen?: () => void;
  fileName?: string;
  language?: string;
  className?: string;
  readOnly?: boolean;
}