// File: src/components/Editor/index.ts
// Directory: src/components/Editor/

import EditorBase from './Editor';
import EditorPane from './EditorPane';
import EditorToolbar from './EditorToolbar';
import EditorStatusBar from './EditorStatusBar';

// Create a composable editor with sub-components
type EditorComponent = typeof EditorBase & {
  Pane: typeof EditorPane;
  Toolbar: typeof EditorToolbar;
  StatusBar: typeof EditorStatusBar;
};

const Editor = EditorBase as EditorComponent;
Editor.Pane = EditorPane;
Editor.Toolbar = EditorToolbar;
Editor.StatusBar = EditorStatusBar;

export type { EditorComponent };
export { EditorPane, EditorToolbar, EditorStatusBar };
export default Editor;