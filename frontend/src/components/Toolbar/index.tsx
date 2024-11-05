// src/components/Toolbar/index.tsx
import React from 'react';
import { Menu, Settings, Moon, Sun, Play, Save } from 'lucide-react';
import { useTheme } from '@/context/ThemeContext';

interface ToolbarProps {
  className?: string;
}

export const Toolbar: React.FC<ToolbarProps> = ({ className }) => {
  const { theme, toggleTheme } = useTheme();

  return (
    <div className={`flex items-center h-12 px-4 bg-gray-800 border-b border-gray-700 ${className || ''}`}>
      <div className="flex items-center gap-2">
        <button className="p-2 hover:bg-gray-700 rounded">
          <Menu className="w-5 h-5 text-gray-400" />
        </button>
        <span className="text-gray-200 font-semibold">PyDitor</span>
      </div>
      <div className="flex-1" />
      <div className="flex items-center gap-2">
        <button className="p-2 hover:bg-gray-700 rounded" title="Save (Ctrl+S)">
          <Save className="w-5 h-5 text-gray-400" />
        </button>
        <button className="p-2 hover:bg-gray-700 rounded" title="Run (F5)">
          <Play className="w-5 h-5 text-gray-400" />
        </button>
        <button
          onClick={toggleTheme}
          className="p-2 hover:bg-gray-700 rounded"
          title={`Switch to ${theme === 'dark' ? 'light' : 'dark'} theme`}
        >
          {theme === 'dark' ? (
            <Sun className="w-5 h-5 text-gray-400" />
          ) : (
            <Moon className="w-5 h-5 text-gray-400" />
          )}
        </button>
        <button className="p-2 hover:bg-gray-700 rounded">
          <Settings className="w-5 h-5 text-gray-400" />
        </button>
      </div>
    </div>
  );
};