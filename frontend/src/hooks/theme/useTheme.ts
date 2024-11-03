// File: src/hooks/theme/useTheme.ts
// Directory: src/hooks/theme/

import { useContext } from 'react';
import { ThemeContext, type ThemeMode, type ThemeContextType } from '../../context/theme/ThemeContext';

export const useTheme = (): ThemeContextType => {
  const context = useContext(ThemeContext);
  
  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  
  return context;
};

export type { ThemeMode };