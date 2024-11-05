// src/components/Tabs/styles.ts

import styled from 'styled-components';

export const FileTabContainer = styled.div`
  display: flex;
  background-color: ${props => props.theme.colors.background.secondary};
  padding: 4px 8px;
  border-bottom: 1px solid ${props => props.theme.colors.border};
`;

export const FileTab = styled.div<{ isActive?: boolean }>`
  padding: 6px 12px;
  background-color: ${props => (props.isActive ? props.theme.colors.background.primary : '#444')};
  color: ${props => (props.isActive ? props.theme.colors.accent : '#ddd')};
  border-bottom: 2px solid ${props => (props.isActive ? props.theme.colors.accent : 'transparent')};
  margin-right: 4px;
  cursor: pointer;

  &:hover {
    background-color: #555;
  }
`;
