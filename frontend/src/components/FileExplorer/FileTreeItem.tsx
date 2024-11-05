// src/components/FileExplorer/FileTreeItem.tsx
import React from 'react';
import styled from 'styled-components';
import { ChevronRight, ChevronDown, File, Folder } from 'lucide-react';

interface FileTreeItemProps {
  name: string;
  type: 'file' | 'directory';
  level: number;
  isOpen?: boolean;
  onToggle?: () => void;
  onSelect?: () => void;
  children?: React.ReactNode;
}

const ItemContainer = styled.div<{ level: number }>`
  padding: 3px 0;
  padding-left: ${props => props.level * 16}px;
  display: flex;
  align-items: center;
  cursor: pointer;
  color: ${props => props.theme.colors.foreground.primary};

  &:hover {
    background: ${props => props.theme.colors.background.tertiary};
  }
`;

export const FileTreeItem: React.FC<FileTreeItemProps> = ({
  name,
  type,
  level,
  isOpen,
  onToggle,
  onSelect,
  children
}) => (
  <ItemContainer level={level} onClick={onSelect}>
    {type === 'directory' && (
      isOpen ? 
        <ChevronDown size={16} onClick={onToggle} /> : 
        <ChevronRight size={16} onClick={onToggle} />
    )}
    {type === 'directory' ? <Folder size={16} /> : <File size={16} />}
    <span className="ml-1">{name}</span>
    {isOpen && children}
  </ItemContainer>
);
