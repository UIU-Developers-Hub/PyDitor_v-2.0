// File: src/components/Sidebar/FileTree.tsx
// Directory: src/components/Sidebar/

import React from 'react';
import { useFileSystem } from '../../hooks/useEditor';
import { File, Folder, ChevronRight, ChevronDown } from 'lucide-react';
import type { FileNode } from '../../types/file';
import { cn } from '../../utils/format';

const FileTree: React.FC = () => {
  const { files, selectedFile, selectFile, toggleFolder } = useFileSystem();

  const renderNode = (node: FileNode, level: number = 0) => {
    const isExpanded = node.type === 'folder' && node.isExpanded;
    const isSelected = selectedFile === node.path;

    return (
      <div key={node.path}>
        <div
          className={cn(
            'flex items-center py-1 px-2 cursor-pointer text-gray-300 hover:text-white',
            'hover:bg-gray-700',
            isSelected && 'bg-gray-700 text-white'
          )}
          style={{ paddingLeft: `${level * 16 + 8}px` }}
          onClick={() => {
            if (node.type === 'file') {
              selectFile(node.path);
            } else {
              toggleFolder(node.path);
            }
          }}
        >
          {node.type === 'folder' && (
            <button 
              className="mr-1 text-gray-400 hover:text-white"
              onClick={(e) => {
                e.stopPropagation();
                toggleFolder(node.path);
              }}
            >
              {isExpanded ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
            </button>
          )}
          {node.type === 'folder' ? (
            <Folder size={16} className="mr-2 text-yellow-500" />
          ) : (
            <File size={16} className="mr-2 text-blue-400" />
          )}
          <span className="text-sm truncate">{node.name}</span>
        </div>
        {node.type === 'folder' && isExpanded && node.children && (
          <div>
            {node.children.map((child) => renderNode(child, level + 1))}
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="flex-1 overflow-y-auto py-2 bg-gray-800 dark:bg-gray-900">
      {files.map((file) => renderNode(file, 0))}
    </div>
  );
};

export default FileTree;