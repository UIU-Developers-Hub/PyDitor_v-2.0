// src/context/FileSystemContext.tsx
import React, { createContext, useContext, useState } from 'react';
import { FileNode } from '../types/file';

interface FileSystemContextType {
  files: FileNode[];
  selectedFile: FileNode | null;
  createFile: (name: string, type: 'file' | 'directory', parentId?: string) => void;
  deleteFile: (id: string) => void;
  updateFile: (id: string, content: string) => void;
  selectFile: (file: FileNode) => void;
}

export const FileSystemContext = createContext<FileSystemContextType | null>(null);

export const FileSystemProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [files, setFiles] = useState<FileNode[]>([]);
  const [selectedFile, setSelectedFile] = useState<FileNode | null>(null);

  const createFile = (name: string, type: 'file' | 'directory', parentId?: string) => { // Changed "folder" to "directory"
    const newFile: FileNode = {
      id: Math.random().toString(36).substring(7),
      name,
      type,
      children: type === 'directory' ? [] : undefined // Changed "folder" to "directory"
    };

    if (!parentId) {
      setFiles([...files, newFile]);
      return;
    }

    const updateChildren = (nodes: FileNode[]): FileNode[] => {
      return nodes.map(node => {
        if (node.id === parentId) {
          return {
            ...node,
            children: [...(node.children || []), newFile]
          };
        }
        if (node.children) {
          return {
            ...node,
            children: updateChildren(node.children)
          };
        }
        return node;
      });
    };

    setFiles(updateChildren(files));
  };

  const deleteFile = (id: string) => {
    const removeFile = (nodes: FileNode[]): FileNode[] => {
      return nodes.filter(node => {
        if (node.id === id) {
          return false;
        }
        if (node.children) {
          node.children = removeFile(node.children);
        }
        return true;
      });
    };

    setFiles(removeFile(files));
    if (selectedFile?.id === id) {
      setSelectedFile(null);
    }
  };

  const updateFile = (id: string, content: string) => {
    const updateNode = (nodes: FileNode[]): FileNode[] => {
      return nodes.map(node => {
        if (node.id === id) {
          return { ...node, content };
        }
        if (node.children) {
          return { ...node, children: updateNode(node.children) };
        }
        return node;
      });
    };

    setFiles(updateNode(files));
  };

  const selectFile = (file: FileNode) => {
    setSelectedFile(file);
  };

  return (
    <FileSystemContext.Provider 
      value={{ files, selectedFile, createFile, deleteFile, updateFile, selectFile }}
    >
      {children}
    </FileSystemContext.Provider>
  );
};

export const useFileSystem = () => {
  const context = useContext(FileSystemContext);
  if (!context) {
    throw new Error('useFileSystem must be used within a FileSystemProvider');
  }
  return context;
};
