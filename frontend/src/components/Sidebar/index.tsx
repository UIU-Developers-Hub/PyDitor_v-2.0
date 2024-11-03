// File: src/components/Sidebar/index.tsx
// Directory: src/components/Sidebar/

import React from 'react';
import SearchPanel from './SearchPanel';
import FileExplorer from './FileExplorer';

const Sidebar: React.FC = () => {
  return (
    <div className="flex flex-col h-full bg-gray-800 dark:bg-gray-900">
      <SearchPanel />
      <FileExplorer />
    </div>
  );
};

export default Sidebar;