// File: src/components/Sidebar/SearchPanel.tsx
// Directory: src/components/Sidebar/

import React, { useState } from 'react';
import { Search } from 'lucide-react';

const SearchPanel: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState('');

  return (
    <div className="p-4 border-b border-gray-700 bg-gray-800 dark:bg-gray-900">
      <div className="relative">
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Search files..."
          className="w-full pl-8 pr-4 py-1.5 text-sm bg-gray-700 text-white placeholder-gray-400 
                   rounded border border-gray-600 focus:outline-none focus:ring-1 focus:ring-blue-500
                   focus:border-blue-500"
        />
        <Search 
          size={16} 
          className="absolute left-2 top-1/2 transform -translate-y-1/2 text-gray-400" 
        />
      </div>
    </div>
  );
};

export default SearchPanel;