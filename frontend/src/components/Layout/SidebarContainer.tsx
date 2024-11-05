// src/components/Layout/SidebarContainer.tsx
import React from 'react';
import { FileExplorer } from '../Sidebar/FileExplorer';

interface SidebarContainerProps {
  className?: string;
}

export const SidebarContainer: React.FC<SidebarContainerProps> = ({ className }) => {
  return (
    <div className={`flex flex-col bg-gray-800 ${className || ''}`}>
      <FileExplorer />
    </div>
  );
};