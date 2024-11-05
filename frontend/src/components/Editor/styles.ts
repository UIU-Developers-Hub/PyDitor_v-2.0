// src/components/Editor/styles.ts

import styled from 'styled-components';

export const EditorPaneContainer = styled.div`
  flex: 1;
  background-color: ${props => props.theme.colors.background.primary};
  color: #e8e8e8;
  font-family: 'Fira Code', monospace;
  font-size: 16px;
  line-height: 1.5;
  padding: 16px;
  display: flex;
  flex-direction: column;
`;

export const LineNumber = styled.div`
  padding-right: 12px;
  color: #666;
`;

export const CodeArea = styled.pre`
  overflow: auto;
  white-space: pre;
  padding: 0 12px;
`;
