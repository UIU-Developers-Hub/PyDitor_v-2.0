// src/components/Terminal/Terminal.tsx
import React, { useEffect, useRef } from 'react';
import { Terminal as XTerm } from 'xterm';
import { FitAddon } from 'xterm-addon-fit';
import { Terminal as TerminalIcon, X } from 'lucide-react';
import 'xterm/css/xterm.css';

interface TerminalComponentProps {
  onClose?: () => void;
}

const TerminalComponent: React.FC<TerminalComponentProps> = ({ onClose }) => {
  const terminalRef = useRef<HTMLDivElement>(null);
  const xtermRef = useRef<XTerm | null>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const fitAddonRef = useRef<FitAddon | null>(null);

  useEffect(() => {
    const term = new XTerm({
      cursorBlink: true,
      fontSize: 14,
      fontFamily: 'JetBrains Mono, Consolas, monospace',
      theme: {
        background: '#1E1E1E',
        foreground: '#D4D4D4',
        cursor: '#D4D4D4'
      },
    });

    const fitAddon = new FitAddon();
    term.loadAddon(fitAddon);
    xtermRef.current = term;
    fitAddonRef.current = fitAddon;

    if (terminalRef.current) {
      term.open(terminalRef.current);
      fitAddon.fit();
    }

    wsRef.current = new WebSocket('ws://localhost:8000/ws/terminal');

    wsRef.current.onopen = () => {
      term.write('\r\nConnected to terminal server\r\n');
      term.write('\r\nType your commands here...\r\n');
      term.write('\r\n$ ');
    };

    wsRef.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'output') {
        term.write('\r\n' + data.content);
        term.write('\r\n$ ');
      }
    };

    let commandBuffer = '';
    term.onKey(({ key, domEvent }) => {
      const printable = !domEvent.altKey && !domEvent.ctrlKey && !domEvent.metaKey;

      if (domEvent.keyCode === 13) { // Enter key
        if (commandBuffer.trim()) {
          wsRef.current?.send(JSON.stringify({
            type: 'command',
            content: commandBuffer
          }));
        }
        commandBuffer = '';
        term.write('\r\n$ ');
      } else if (domEvent.keyCode === 8) { // Backspace
        if (commandBuffer.length > 0) {
          commandBuffer = commandBuffer.slice(0, -1);
          term.write('\b \b');
        }
      } else if (printable) {
        commandBuffer += key;
        term.write(key);
      }
    });

    const handleResize = () => {
      fitAddonRef.current?.fit();
    };

    window.addEventListener('resize', handleResize);

    return () => {
      term.dispose();
      wsRef.current?.close();
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  return (
    <div className="h-64 bg-[#1E1E1E] rounded-lg overflow-hidden border border-gray-700">
      <div className="h-8 bg-gray-800 flex items-center px-4 justify-between">
        <div className="flex items-center">
          <TerminalIcon className="h-4 w-4 text-gray-400 mr-2" />
          <span className="text-sm text-gray-300">Terminal</span>
        </div>
        {onClose && (
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-white transition-colors"
          >
            <X className="h-4 w-4" />
          </button>
        )}
      </div>
      <div ref={terminalRef} className="h-[calc(100%-2rem)]" />
    </div>
  );
};

export default TerminalComponent;