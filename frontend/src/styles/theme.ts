// src/styles/theme.ts
import 'styled-components';

const theme = {
  colors: {
    primary: '#3498db',
    secondary: '#2ecc71',
    tertiary: '#e74c3c',
    activityBar: '#34495e',
    statusBar: '#1abc9c',
    sideBar: '#8e44ad',
    terminal: '#d35400',
    border: '#7f8c8d',
    foreground: {
      primary: '#ecf0f1',
      secondary: '#bdc3c7',
      active: '#2980b9',
    },
    background: {
      primary: '#2c3e50',
      secondary: '#34495e',
      tertiary: '#22313f',
      sideBar: '#8e44ad',
      statusBar: '#d0d0d0',
    },
    accent: '#f39c12',
    selection: '#95a5a6',
  },
  spacing: {
    small: '8px',
    medium: '16px',
    large: '32px',
    xlarge: '48px',
  },
  borderRadius: '4px',
  typography: {
    fontFamily: "'JetBrains Mono', 'Fira Code', monospace",
    fontSize: '16px',
  },
};

export default theme;