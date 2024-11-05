// src/App.tsx
import React, { useState } from 'react';
import { ThemeProvider } from 'styled-components';
import GlobalStyles from './styles/GlobalStyles';
import theme from './styles/theme';
import { FileSystemProvider } from './context/FileSystemContext';
import { SidebarContainer } from './components/Sidebar/SidebarContainer';
import { EditorPane } from './components/Editor/EditorPane';
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

  return (
    <ThemeProvider theme={theme}>
      <GlobalStyles />
      <FileSystemProvider>
        <div style={{ display: 'flex', height: '100vh' }}> {/* Adjust the app container */}
          <SidebarContainer
            files={files}
            onAddFile={addFile}
            onDeleteFile={deleteFile}
            onRenameFile={renameFile}
          />
          <main style={{ flex: 1, backgroundColor: '#1e1e1e' }}> {/* Use background similar to VSCode */}
            <EditorPane />
          </main>
        </div>
      </FileSystemProvider>
    </ThemeProvider>
  );
};

export default App;
