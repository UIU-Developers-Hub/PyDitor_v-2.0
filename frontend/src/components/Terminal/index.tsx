// src/components/Terminal/index.tsx
import React, { useEffect, useRef } from 'react';
import { Terminal as XTerm } from 'xterm';
import { FitAddon } from 'xterm-addon-fit';
import { WebLinksAddon } from 'xterm-addon-web-links';
import styled from 'styled-components';
import 'xterm/css/xterm.css';

// Styled-component with explicit typing for theme properties
const TerminalContainer = styled.div`
  height: 300px;
  background: ${(props) => props.theme.colors.terminal || props.theme.colors.background.primary}; // Ensure terminal is defined in theme
  padding: 8px;
`;

interface TerminalProps {
  onData?: (data: string) => void;
}

export const Terminal: React.FC<TerminalProps> = ({ onData }) => {
  const terminalRef = useRef<HTMLDivElement>(null);
  const xtermRef = useRef<XTerm | null>(null);

  useEffect(() => {
    if (terminalRef.current) {
      const term = new XTerm({
        theme: {
          background: '#1e1e1e',
          foreground: '#d4d4d4',
          cursor: '#d4d4d4'
        },
        fontSize: 14,
        fontFamily: 'JetBrains Mono'
      });

      const fitAddon = new FitAddon();
      term.loadAddon(fitAddon);
      term.loadAddon(new WebLinksAddon());

      term.open(terminalRef.current);
      fitAddon.fit();

      term.onData((data: string) => {
        onData?.(data);
      });

      xtermRef.current = term;

      return () => {
        term.dispose();
      };
    }
  }, [onData]);

  return <TerminalContainer ref={terminalRef} />;
};
