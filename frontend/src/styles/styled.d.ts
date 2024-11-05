// src/styles/styled.d.ts
import 'styled-components';

declare module 'styled-components' {
  export interface DefaultTheme {
    colors: {
      primary: string;
      secondary: string;
      tertiary: string;
      activityBar: string;
      statusBar: string;
      sideBar: string;
      terminal: string;
      border: string;
      accent: string;
      selection: string;
      foreground: {
        primary: string;
        secondary: string;
        active: string;
      };
      background: {
        primary: string;
        secondary: string;
        tertiary: string;
        sideBar: string;
        statusBar: string;
      };
    };
    spacing: {
      small: string;
      medium: string;
      large: string;
      xlarge: string;
    };
    borderRadius: string;
    typography: {
      fontFamily: string;
      fontSize: string;
    };
  }
}
