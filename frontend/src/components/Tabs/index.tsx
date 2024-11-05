// src/components/Tabs/index.tsx

import React from 'react';
import { FileTabContainer, FileTab } from './styles';

interface TabProps {
  tabs: string[];
  activeTab: string;
  onTabClick: (tabName: string) => void;
}

const Tabs: React.FC<TabProps> = ({ tabs, activeTab, onTabClick }) => {
  return (
    <FileTabContainer>
      {tabs.map((tabName) => (
        <FileTab 
          key={tabName} 
          isActive={activeTab === tabName}
          onClick={() => onTabClick(tabName)}
        >
          {tabName}
        </FileTab>
      ))}
    </FileTabContainer>
  );
};

export default Tabs;
