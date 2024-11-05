// src/components/Sidebar/index.tsx
import { FC, ReactNode } from 'react'; // Removed React import
import { SidebarContainer, SidebarItem, IconContainer } from './styles';
import { FileText, Folder } from 'lucide-react';

interface SidebarProps {
  className?: string;
  children?: ReactNode;
}

const Sidebar: FC<SidebarProps> = ({ className, children }) => {
  return (
    <SidebarContainer className={className}>
      <SidebarItem>
        <IconContainer>
          <Folder size={16} />
        </IconContainer>
        src
      </SidebarItem>
      <SidebarItem>
        <IconContainer>
          <FileText size={16} />
        </IconContainer>
        README.md
      </SidebarItem>
      {children}
    </SidebarContainer>
  );
};

export default Sidebar;
