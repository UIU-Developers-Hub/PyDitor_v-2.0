// File: src/components/Toolbar/Toolbar.tsx
import React from 'react';
import { Play, Save, FileText, Settings } from 'lucide-react';

interface ToolbarProps {
  onRun: () => void;
  onSave: () => void;
  onNewFile: () => void;
}

const Toolbar: React.FC<ToolbarProps> = ({ onRun, onSave, onNewFile }) => {
  return (
    <div className="h-12 bg-gray-800 border-b border-gray-700 flex items-center px-4 justify-between">
      <div className="flex items-center space-x-2">
        <span className="text-white font-medium">PyDitor</span>
      </div>
      
      <div className="flex items-center space-x-4">
        <button 
          onClick={onNewFile}
          className="p-2 hover:bg-gray-700 rounded-md text-gray-300 hover:text-white"
          title="New File"
        >
          <FileText size={20} />
        </button>
        
        <button 
          onClick={onSave}
          className="p-2 hover:bg-gray-700 rounded-md text-gray-300 hover:text-white"
          title="Save"
        >
          <Save size={20} />
        </button>
        
        <button 
          onClick={onRun}
          className="px-4 py-1.5 bg-green-600 hover:bg-green-700 rounded-md flex items-center space-x-2 text-white"
        >
          <Play size={16} />
          <span>Run</span>
        </button>

        <button 
          className="p-2 hover:bg-gray-700 rounded-md text-gray-300 hover:text-white"
          title="Settings"
        >
          <Settings size={20} />
        </button>
      </div>
    </div>
  );
};

export default Toolbar;