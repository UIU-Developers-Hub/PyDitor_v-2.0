// src/App.tsx
import React, { useState, useRef } from 'react';
import { ThemeProvider } from 'styled-components';
import GlobalStyles from './styles/GlobalStyles';
import theme from './styles/theme';
import { FileSystemProvider } from './context/FileSystemContext';
import { SidebarContainer } from './components/Sidebar/SidebarContainer';
import { EditorPane } from './components/Editor/EditorPane';
import CommandPalette from './components/Terminal/CommandPalette';
import Terminal from './components/Terminal/Terminal'; // Import Terminal as default
import { FileNode } from './types/file';

const initialFiles: FileNode[] = [
  {
    id: '1',
    name: 'src',
    type: 'directory',
    children: [{ id: '2', name: 'index.tsx', type: 'file' }],
  },
  {
    id: '3',
    name: 'README.md',
    type: 'file',
  },
];

const App: React.FC = () => {
  const [files, setFiles] = useState<FileNode[]>(initialFiles);
  const [isCommandPaletteVisible, setIsCommandPaletteVisible] = useState(false);
  const terminalRef = useRef<{ clearTerminal: () => void; writeToTerminal: (text: string) => void } | null>(null);

  const addFile = (name: string, type: 'file' | 'directory') => {
    setFiles([...files, { id: Math.random().toString(), name, type }]);
  };

  const deleteFile = (id: string) => {
    setFiles(files.filter(file => file.id !== id));
  };

  const renameFile = (id: string, newName: string) => {
    setFiles(
      files.map(file =>
        file.id === id ? { ...file, name: newName } : file
      )
    );
  };

  // Command Palette actions
  const commands = [
    { name: 'Add New File', action: () => addFile('New File', 'file') },
    { name: 'Clear Terminal', action: () => terminalRef.current?.clearTerminal() },
    { name: 'Write to Terminal', action: () => terminalRef.current?.writeToTerminal('Hello from Command Palette\n') },
  ];

  const toggleCommandPalette = () => {
    setIsCommandPaletteVisible(prev => !prev);
  };

  React.useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.ctrlKey && e.shiftKey && e.key === 'P') {
        toggleCommandPalette();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  return (
    <ThemeProvider theme={theme}>
      <GlobalStyles />
      <FileSystemProvider>
        <div style={{ display: 'flex', height: '100vh' }}>
          <SidebarContainer
            files={files}
            onAddFile={addFile}
            onDeleteFile={deleteFile}
            onRenameFile={renameFile}
          />
          <main style={{ flex: 1, display: 'flex', flexDirection: 'column', backgroundColor: '#1e1e1e' }}>
            {/* EditorPane occupies the top part of main */}
            <div style={{ flex: 1, overflow: 'auto' }}>
              <EditorPane />
            </div>
            {/* Terminal occupies the bottom part of main */}
            <div style={{ height: '300px', borderTop: '1px solid #333' }}>
              <Terminal ref={terminalRef} />
            </div>
          </main>
        </div>
        {/* Render Command Palette conditionally */}
        {isCommandPaletteVisible && (
          <CommandPalette
            commands={commands}
            isVisible={isCommandPaletteVisible}
            onClose={() => setIsCommandPaletteVisible(false)}
          />
        )}
      </FileSystemProvider>
    </ThemeProvider>
  );
};

export default App;
