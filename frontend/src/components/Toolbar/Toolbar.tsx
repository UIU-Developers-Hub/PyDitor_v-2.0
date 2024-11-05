// src/components/Toolbar/index.tsx
import React from 'react';
import { Menu, Settings, Moon, Sun } from 'lucide-react';
import { useTheme } from '@/context/ThemeContext';

interface ToolbarProps {
  className?: string;
}

export const Toolbar: React.FC<ToolbarProps> = ({ className }) => {
  const { theme, toggleTheme } = useTheme();

  return (
    <div className={`flex items-center px-2 h-12 border-b border-gray-700 ${className || ''}`}>
      <button className="p-2 hover:bg-gray-700 rounded-lg">
        <Menu className="w-5 h-5 text-gray-400" />
      </button>
      <div className="flex-1" />
      <button
        onClick={toggleTheme}
        className="p-2 hover:bg-gray-700 rounded-lg"
        title={`Switch to ${theme === 'dark' ? 'light' : 'dark'} theme`}
      >
        {theme === 'dark' ? (
          <Sun className="w-5 h-5 text-gray-400" />
        ) : (
          <Moon className="w-5 h-5 text-gray-400" />
        )}
      </button>
      <button className="p-2 hover:bg-gray-700 rounded-lg">
        <Settings className="w-5 h-5 text-gray-400" />
      </button>
    </div>
  );
};
export default Toolbar;