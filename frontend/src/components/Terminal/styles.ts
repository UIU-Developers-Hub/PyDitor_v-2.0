// src/components/Terminal/styles.ts
import styled, { css } from 'styled-components';

export const TerminalContainer = styled.div`
  flex-grow: 1;
  width: 100%;
  display: flex;
  flex-direction: column;
  background: ${(props) => props.theme.colors.terminal || props.theme.colors.background.primary};
  border-top: 1px solid #444;
  position: relative;
  display: flex;
`;

export const TerminalHeader = styled.div`
  display: flex;
  align-items: center;
  padding: 0 8px;
  background-color: #2d2d2d;
  border-bottom: 1px solid #444;
  color: #d4d4d4;
  font-size: 13px;
`;

export const TerminalTab = styled.div<{ $active?: boolean }>`
  display: flex;
  align-items: center;
  padding: 8px 12px;
  cursor: pointer;
  color: #d4d4d4;
  font-weight: bold;
  transition: background-color 0.3s ease, color 0.3s ease;

  &:hover {
    background-color: #333;
    color: #ffffff;
  }

  ${({ $active }) =>
    $active &&
    css`
      border-bottom: 2px solid #007acc;
      color: #ffffff;
      background-color: #333;
    `}

  svg {
    margin-left: 8px;
    font-size: 14px;
    cursor: pointer;
    transition: color 0.2s;

    &:hover {
      color: #ff6666;
    }
  }
`;

export const Toolbar = styled.div`
  margin-left: auto;
  display: flex;
  align-items: center;
`;

export const FilterInput = styled.input`
  padding: 4px 8px;
  margin-right: 8px;
  border: 1px solid #555;
  border-radius: 4px;
  background-color: #1e1e1e;
  color: #d4d4d4;
  font-size: 13px;
  width: 250px;

  &::placeholder {
    color: #888;
  }

  &:focus {
    outline: none;
    border-color: #007acc;
  }
`;

export const ToolbarButton = styled.button<{ $active?: boolean }>`
  background: none;
  border: none;
  color: ${(props) => (props.$active ? '#ffffff' : '#d4d4d4')};
  margin-right: 8px;
  cursor: pointer;
  padding: 4px;
  position: relative;

  svg {
    fill: ${(props) => (props.$active ? '#007acc' : '#d4d4d4')};
    width: 20px;
    height: 20px;
    transition: fill 0.2s ease;
  }

  &:hover {
    color: #ffffff;

    svg {
      fill: #ffffff;
    }
  }

  &:hover::after {
    content: attr(title);
    position: absolute;
    bottom: -24px;
    left: 50%;
    transform: translateX(-50%);
    background: #333;
    color: #ffffff;
    font-size: 12px;
    padding: 4px 8px;
    border-radius: 4px;
    white-space: nowrap;
    opacity: 0.9;
    z-index: 1;
  }
`;

export const TerminalBody = styled.div`
  flex-grow: 1;
  padding: 12px;
  background: ${(props) => props.theme.colors.terminal || props.theme.colors.background.primary};
  color: ${(props) => props.theme.colors.foreground.primary};
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  font-family: ${(props) => props.theme.typography.fontFamily};
  font-size: ${(props) => props.theme.typography.fontSize};
  border-left: 1px solid #444;
  border-right: 1px solid #444;
  border-bottom: 1px solid #444;

  ::-webkit-scrollbar {
    width: 8px;
  }
  ::-webkit-scrollbar-thumb {
    background-color: #555;
    border-radius: 4px;
  }
  ::-webkit-scrollbar-thumb:hover {
    background-color: #666;
  }
  ::-webkit-scrollbar-track {
    background: #2d2d2d;
  }
`;

export const Resizer = styled.div`
  height: 4px;
  background-color: #333;
  cursor: row-resize;
  position: absolute;
  bottom: 0;
  width: 100%;
`;

export const TerminalsSidebar = styled.div`
  width: 200px;
  background-color: #2d2d2d;
  border-right: 1px solid #444;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
`;

export const SidebarTerminalItem = styled.div<{ $active?: boolean }>`
  padding: 8px 12px;
  cursor: pointer;
  color: ${(props) => (props.$active ? '#ffffff' : '#d4d4d4')};
  background-color: ${(props) => (props.$active ? '#333' : 'transparent')};
  display: flex;
  align-items: center;
  justify-content: space-between;
  transition: background-color 0.3s ease, color 0.3s ease;

  &:hover {
    background-color: #333;
    color: #ffffff;
  }

  svg {
    cursor: pointer;
    font-size: 14px;
    color: #ff6666;
    transition: color 0.2s;

    &:hover {
      color: #ff4d4d;
    }
  }
`;
