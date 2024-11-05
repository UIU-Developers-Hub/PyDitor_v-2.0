// src/components/Terminal/index.tsx
import { useEffect, useRef, useImperativeHandle, forwardRef, useCallback } from 'react';
import { Terminal as XTerm } from 'xterm';
import { FitAddon } from 'xterm-addon-fit';
import { WebLinksAddon } from 'xterm-addon-web-links';
import { TerminalContainer } from './styles'; // Corrected import path to use './styles'
import 'xterm/css/xterm.css';

interface TerminalProps {
  onData?: (data: string) => void;
  onResize?: () => void;
  commands?: { [command: string]: () => void };
}

export const Terminal = forwardRef(({ onData, onResize, commands }: TerminalProps, ref) => {
  const terminalRef = useRef<HTMLDivElement>(null);
  const xtermRef = useRef<XTerm | null>(null);
  const fitAddon = useRef(new FitAddon());

  const handleResize = useCallback(() => {
    fitAddon.current.fit();
    onResize?.();
  }, [onResize]);

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

      term.loadAddon(fitAddon.current);
      term.loadAddon(new WebLinksAddon());

      term.open(terminalRef.current);
      fitAddon.current.fit();

      term.onData((data: string) => {
        if (commands && data in commands) {
          commands[data]();
        }
        onData?.(data);
      });

      xtermRef.current = term;

      window.addEventListener('resize', handleResize);
      return () => {
        term.dispose();
        window.removeEventListener('resize', handleResize);
      };
    }
  }, [onData, commands, handleResize]);

  useImperativeHandle(ref, () => ({
    clearTerminal: () => {
      xtermRef.current?.clear();
    },
    writeToTerminal: (text: string) => {
      xtermRef.current?.write(text);
    },
  }));

  return <TerminalContainer ref={terminalRef} />;
});
