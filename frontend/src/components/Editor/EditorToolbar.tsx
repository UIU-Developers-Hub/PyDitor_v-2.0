// File: src/components/Editor/EditorToolbar.tsx
// Directory: src/components/Editor/

import React from 'react';
import { Save, Play, Settings, Moon, Sun, Download, Share, Copy } from 'lucide-react';
import { useTheme } from '../../hooks/theme/useTheme';

const EditorToolbar: React.FC = () => {
  const { theme, toggleTheme } = useTheme();

  return (
    <div className="h-12 flex items-center justify-between px-4 bg-gray-800 dark:bg-gray-900 border-b border-gray-700">
      {/* Left side actions */}
      <div className="flex items-center space-x-2">
        <button className="p-2 hover:bg-gray-700 rounded-md flex items-center gap-2 text-sm text-white">
          <Save size={16} className="text-white" />
          <span>Save</span>
        </button>
        <button className="p-2 hover:bg-gray-700 rounded-md flex items-center gap-2 text-sm text-white">
          <Play size={16} className="text-white" />
          <span>Run</span>
        </button>
        <div className="h-4 w-px bg-gray-600" />
        <button className="p-2 hover:bg-gray-700 rounded-md">
          <Copy size={16} className="text-white" />
        </button>
        <button className="p-2 hover:bg-gray-700 rounded-md">
          <Download size={16} className="text-white" />
        </button>
        <button className="p-2 hover:bg-gray-700 rounded-md">
          <Share size={16} className="text-white" />
        </button>
      </div>

      {/* Right side actions */}
      <div className="flex items-center space-x-2">
        <button
          onClick={toggleTheme}
          className="p-2 hover:bg-gray-700 rounded-md text-white"
          title={theme === 'light' ? 'Switch to dark mode' : 'Switch to light mode'}
        >
          {theme === 'light' ? <Moon size={16} /> : <Sun size={16} />}
        </button>
        <button className="p-2 hover:bg-gray-700 rounded-md">
          <Settings size={16} className="text-white" />
        </button>
      </div>
    </div>
  );
};

export default EditorToolbar;