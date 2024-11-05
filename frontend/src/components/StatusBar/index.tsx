// src/components/StatusBar/index.tsx

import React from 'react';
import { StatusBarContainer } from './styles';

const StatusBar: React.FC = () => {
  return (
    <StatusBarContainer>
      <span>Line 1, Column 1</span>
      <span>UTF-8</span>
    </StatusBarContainer>
  );
};

export default StatusBar;
