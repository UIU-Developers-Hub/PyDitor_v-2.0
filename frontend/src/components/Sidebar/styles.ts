// src/components/Sidebar/styles.ts
import styled from 'styled-components';

export const SidebarContainer = styled.div<{ $level?: number }>`
  width: 250px; // Fixed width for the sidebar
  height: 100%;
  background: ${props => props.theme.colors.background.sideBar};
  color: ${props => props.theme.colors.foreground.primary};
  display: flex;
  flex-direction: column;
  padding: 16px;
  border-right: 1px solid ${props => props.theme.colors.border}; // Optional: Add a border to the right
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1); // Optional: Add a subtle shadow
`;

export const SidebarItem = styled.div`
  display: flex;
  align-items: center;
  padding: 8px;
  cursor: pointer;
  border-radius: ${({ theme }) => theme.borderRadius};
  transition: background 0.2s;

  &:hover {
    background: ${({ theme }) => theme.colors.selection};
  }
`;

export const IconContainer = styled.div`
  margin-right: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
`;
