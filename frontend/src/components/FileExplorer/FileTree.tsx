// src/components/FileExplorer/FileTree.tsx

import React, { useState } from 'react';
import { FileTreeItem } from './FileTreeItem';
import styled from 'styled-components';

interface File {
  name: string;
  type: 'file' | 'directory';
  children?: File[];
}

interface FileTreeProps {
  files: File[];
}

const TreeContainer = styled.div`
  display: flex;
  flex-direction: column;
  padding: 8px;
`;

export const FileTree: React.FC<FileTreeProps> = ({ files }) => {
  const [expandedFolders, setExpandedFolders] = useState<{ [key: string]: boolean }>({});

  const toggleFolder = (name: string) => {
    setExpandedFolders(prev => ({ ...prev, [name]: !prev[name] }));
  };

  return (
    <TreeContainer>
      {files.map((file, index) => (
        <FileTreeItem
          key={index}
          name={file.name}
          type={file.type}
          level={0}
          isOpen={expandedFolders[file.name]}
          onToggle={() => toggleFolder(file.name)}
        >
          {file.children && expandedFolders[file.name] && (
            <div style={{ paddingLeft: 16 }}>
              <FileTree files={file.children} /> {/* Render child files recursively */}
            </div>
          )}
        </FileTreeItem>
      ))}
    </TreeContainer>
  );
};
