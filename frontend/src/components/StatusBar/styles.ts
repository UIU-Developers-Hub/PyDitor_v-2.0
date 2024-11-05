// src/components/StatusBar/styles.ts

import styled from 'styled-components';

export const StatusBarContainer = styled.div`
  height: 24px;
  background-color: ${props => props.theme.colors.statusBar};
  color: #999;
  font-size: 13px;
  padding: 4px 8px;
  display: flex;
  align-items: center;
  justify-content: space-between;
`;
