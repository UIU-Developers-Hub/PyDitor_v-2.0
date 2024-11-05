// src/components/Layout/MainLayout.tsx
import React from 'react';
import styled from 'styled-components';
import { SidebarContainer } from './SidebarContainer';

const LayoutContainer = styled.div.attrs({
  className: 'flex h-screen'
})`
  background-color: ${props => props.theme.colors.background.primary};
`;

export const MainLayout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return (
    <LayoutContainer>
      <SidebarContainer />
      <main className="flex-1">
        {children}
      </main>
    </LayoutContainer>
  );
};