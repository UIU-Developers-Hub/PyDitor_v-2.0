// src/components/Terminal/Terminal.tsx
import { useEffect, useRef, useImperativeHandle, forwardRef, useCallback, useState } from 'react';
import { Terminal as XTerm } from 'xterm';
import { FitAddon } from 'xterm-addon-fit';
import { WebLinksAddon } from 'xterm-addon-web-links';
import { AiOutlineClear, AiOutlineDown, AiOutlineSync, AiOutlinePlus, AiOutlineClose } from 'react-icons/ai';
import {
  TerminalContainer, TerminalHeader, TerminalTab, TerminalBody,
  Toolbar, FilterInput, ToolbarButton, Resizer, TerminalsSidebar, SidebarTerminalItem
} from './styles';
import 'xterm/css/xterm.css';

interface TerminalProps {
  onData?: (data: string) => void;
  commands?: { [command: string]: () => void };
}

interface TerminalInstance {
  id: number;
  name: string;
  xterm: XTerm;
}

const Terminal = forwardRef(({ onData, commands = {} }: TerminalProps, ref) => {
  const [terminals, setTerminals] = useState<TerminalInstance[]>([]);
  const [activeTab, setActiveTab] = useState<'TERMINAL' | 'PROBLEMS' | 'OUTPUT' | 'DEBUG_CONSOLE'>('TERMINAL');
  const [activeTerminalId, setActiveTerminalId] = useState<number | null>(null);
  const [autoScroll, setAutoScroll] = useState(true);
  const [isResizing, setIsResizing] = useState(false);
  const terminalRefs = useRef<{ [id: number]: HTMLDivElement | null }>({});

  // Creates a new terminal instance
  const createTerminal = useCallback(() => {
    const newId = Date.now();
    const term = new XTerm({
      theme: { background: '#1e1e1e', foreground: '#d4d4d4', cursor: '#d4d4d4' },
      fontSize: 14,
      fontFamily: 'JetBrains Mono'
    });

    const fitAddon = new FitAddon();
    term.loadAddon(fitAddon);
    term.loadAddon(new WebLinksAddon());

    const terminalInstance = {
      id: newId,
      name: `Terminal ${terminals.length + 1}`,
      xterm: term,
    };

    setTerminals((prev) => [...prev, terminalInstance]);
    setActiveTerminalId(newId);

    setTimeout(() => {
      if (terminalRefs.current[newId]) {
        term.open(terminalRefs.current[newId]!);
        fitAddon.fit();
      }
    }, 0);

    term.onData((data: string) => {
      if (data.trim() === 'clear') term.clear();
      else commands[data]?.();
      onData?.(data);

      if (autoScroll) term.scrollToBottom();
    });
  }, [commands, onData, autoScroll, terminals]);

  // Close a terminal instance
  const closeTerminal = (id: number) => {
    setTerminals((prev) => prev.filter((term) => term.id !== id));
    if (activeTerminalId === id) {
      const remaining = terminals.filter((term) => term.id !== id);
      setActiveTerminalId(remaining.length ? remaining[0].id : null);
    }
  };

  // Handle resizing of terminal container
  const handleResizing = (e: MouseEvent) => {
    if (isResizing) {
      const height = window.innerHeight - e.clientY;
      terminalRefs.current[activeTerminalId!]?.parentElement?.style.setProperty('height', `${height}px`);
    }
  };

  const handleResizeStart = (e: React.MouseEvent) => {
    e.preventDefault();
    setIsResizing(true);
    document.addEventListener('mousemove', handleResizing);
    document.addEventListener('mouseup', handleResizeEnd);
  };

  const handleResizeEnd = () => {
    setIsResizing(false);
    document.removeEventListener('mousemove', handleResizing);
    document.removeEventListener('mouseup', handleResizeEnd);
  };

  const scrollToBottom = () => {
    const activeTerminal = terminals.find((term) => term.id === activeTerminalId);
    activeTerminal?.xterm.scrollToBottom();
  };

  const toggleAutoScroll = () => setAutoScroll((prev) => !prev);

  useEffect(() => {
    if (terminals.length === 0) createTerminal();
  }, [createTerminal]);

  useImperativeHandle(ref, () => ({
    clearTerminal: () => {
      const activeTerminal = terminals.find((term) => term.id === activeTerminalId);
      activeTerminal?.xterm.clear();
    },
    writeToTerminal: (text: string) => {
      const activeTerminal = terminals.find((term) => term.id === activeTerminalId);
      activeTerminal?.xterm.write(text);
    },
  }));

  // Renders content based on the active tab
  const renderTabContent = () => {
    switch (activeTab) {
      case 'TERMINAL':
        return (
          <TerminalBody>
            {activeTerminalId && (
              <div ref={(ref) => (terminalRefs.current[activeTerminalId] = ref)} style={{ height: '100%' }} />
            )}
          </TerminalBody>
        );
      case 'PROBLEMS':
        return (
          <TerminalBody>
            <p>🚨 Error: Cannot find module 'express' in /src/server.ts</p>
            <p>⚠️ Warning: Unused variable 'foo' in /src/app.ts</p>
          </TerminalBody>
        );
      case 'OUTPUT':
        return (
          <TerminalBody>
            <p>Build started...</p>
            <p>Build succeeded. Serving on localhost:3000</p>
          </TerminalBody>
        );
      case 'DEBUG_CONSOLE':
        return (
          <TerminalBody>
            <p>Debug initialized.</p>
            <p>Breakpoint set in /src/utils.ts at line 42</p>
          </TerminalBody>
        );
      default:
        return null;
    }
  };

  return (
    <TerminalContainer>
      <TerminalHeader>
        {/* Static Tabs */}
        <TerminalTab active={activeTab === 'PROBLEMS'} onClick={() => setActiveTab('PROBLEMS')}>PROBLEMS</TerminalTab>
        <TerminalTab active={activeTab === 'OUTPUT'} onClick={() => setActiveTab('OUTPUT')}>OUTPUT</TerminalTab>
        <TerminalTab active={activeTab === 'DEBUG_CONSOLE'} onClick={() => setActiveTab('DEBUG_CONSOLE')}>DEBUG CONSOLE</TerminalTab>
        <TerminalTab active={activeTab === 'TERMINAL'} onClick={() => setActiveTab('TERMINAL')}>TERMINAL</TerminalTab>

        {/* Toolbar with Action Buttons */}
        <Toolbar>
          <ToolbarButton onClick={createTerminal} title="New Terminal">
            <AiOutlinePlus />
          </ToolbarButton>
          <FilterInput placeholder="Filter (e.g. text, **/*.ts, **/node_modules/**)" />
          <ToolbarButton onClick={() => terminals[0]?.xterm.clear()} title="Clear Terminal">
            <AiOutlineClear />
          </ToolbarButton>
          <ToolbarButton onClick={scrollToBottom} title="Scroll to Bottom">
            <AiOutlineDown />
          </ToolbarButton>
          <ToolbarButton onClick={toggleAutoScroll} title={`Auto-scroll: ${autoScroll ? 'On' : 'Off'}`} active={autoScroll}>
            <AiOutlineSync />
          </ToolbarButton>
        </Toolbar>
      </TerminalHeader>

      <div style={{ display: 'flex', height: '100%' }}>
        {/* Sidebar for terminal instances */}
        <TerminalsSidebar>
          {terminals.map((term) => (
            <SidebarTerminalItem
              key={term.id}
              active={term.id === activeTerminalId}
              onClick={() => {
                setActiveTab('TERMINAL');
                setActiveTerminalId(term.id);
              }}
            >
              {term.name}
              <AiOutlineClose onClick={() => closeTerminal(term.id)} style={{ marginLeft: 8, cursor: 'pointer' }} />
            </SidebarTerminalItem>
          ))}
        </TerminalsSidebar>

        {/* Main content area */}
        {renderTabContent()}
      </div>

      <Resizer
        onMouseDown={handleResizeStart}
        style={{ cursor: isResizing ? 'row-resize' : 'default' }}
      />
    </TerminalContainer>
  );
});

export default Terminal;
