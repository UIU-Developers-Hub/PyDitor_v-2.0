// src/components/Terminal/Terminal.tsx
import React, { useEffect, useRef, useImperativeHandle, forwardRef, useCallback, useState } from 'react';
import { Terminal as XTerm } from 'xterm';
import { FitAddon } from 'xterm-addon-fit';
import { WebLinksAddon } from 'xterm-addon-web-links';
import debounce from 'lodash.debounce';
import { AiOutlineClear, AiOutlineDown, AiOutlineSync, AiOutlinePlus, AiOutlineClose } from 'react-icons/ai';
import { useDispatch } from 'react-redux';
import { setActiveSession, addSession, removeSession } from '@/store/terminalSlice';
import {
  TerminalContainer, TerminalHeader, TerminalTab, TerminalBody,
  Toolbar, FilterInput, ToolbarButton, Resizer, TerminalsSidebar, SidebarTerminalItem
} from './styles';
import 'xterm/css/xterm.css';
import { TerminalService } from '@/services/terminalService';

const LOCAL_STORAGE_KEYS = {
  TERMINALS: 'terminals',
  ACTIVE_TAB: 'activeTab',
  AUTO_SCROLL: 'autoScroll',
  TERMINAL_CONTENT: 'terminalContent'
};

// Debounced local storage save function for performance
const saveToLocalStorage = debounce((key: string, data: any) => {
  localStorage.setItem(key, JSON.stringify(data));
}, 500);

const loadFromLocalStorage = (key: string) => {
  const data = localStorage.getItem(key);
  return data ? JSON.parse(data) : null;
};

interface TerminalProps {
  onData?: (data: string) => void;
  commands?: { [command: string]: () => void };
}

interface TerminalInstance {
  id: number;
  name: string;
  xterm: XTerm;
  service: TerminalService;
}

const Terminal = forwardRef(({ onData, commands = {} }: TerminalProps, ref) => {
  const dispatch = useDispatch();
  const [terminals, setTerminals] = useState<TerminalInstance[]>([]);
  const [activeTab, setActiveTab] = useState<'TERMINAL' | 'PROBLEMS' | 'OUTPUT' | 'DEBUG_CONSOLE'>('TERMINAL');
  const [activeTerminalId, setActiveTerminalId] = useState<number | null>(null);
  const [autoScroll, setAutoScroll] = useState<boolean>(true);
  const [isResizing, setIsResizing] = useState(false);
  const terminalRefs = useRef<{ [id: number]: HTMLDivElement | null }>({});
  const terminalContentRef = useRef<{ [id: number]: string }>({});
  const [authError, setAuthError] = useState<string | null>(null);

  const saveTerminalContent = useCallback((id: number, content: string) => {
    terminalContentRef.current[id] = content;
    saveToLocalStorage(LOCAL_STORAGE_KEYS.TERMINAL_CONTENT, terminalContentRef.current);
  }, []);

  // Connect to terminal service when a terminal is active
  useEffect(() => {
    if (activeTerminalId) {
      const service = new TerminalService(
        activeTerminalId.toString(),
        (data) => {
          const activeTerminal = terminals.find(term => term.id === activeTerminalId);
          if (activeTerminal?.xterm) {
            activeTerminal.xterm.write(data);
          }
        }
      );

      // Handle auth error
      service.connect();

      // Handle WebSocket close event
      service.addCloseListener((event) => {
        if (event.code === 4003) {
          setAuthError('Authentication failed. Please log in again.');
        }
      });

      return () => {
        service.disconnect();
      };
    }
  }, [activeTerminalId, terminals]);

  // Show auth error if present
  if (authError) {
    return (
      <div className="terminal-error">
        <p>{authError}</p>
        <button onClick={() => window.location.href = '/login'}>
          Go to Login
        </button>
      </div>
    );
  }

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

    const terminalService = new TerminalService(
      `${newId}`,
      (data: string) => term.write(data)  // Adjusted to match the expected type
    );
    terminalService.connect();

    const terminalInstance: TerminalInstance = {
      id: newId,
      name: `Terminal ${terminals.length + 1}`,
      xterm: term,
      service: terminalService
    };

    term.onData((data: string) => {
      if (data.trim() === 'clear') {
        term.clear();
        terminalContentRef.current[newId] = '';
      } else {
        if (commands[data]) {
          commands[data]?.();
        } else {
          onData?.(data);
          terminalInstance.service.sendInput(data);
          terminalContentRef.current[newId] = (terminalContentRef.current[newId] || '') + data;
        }
      }
      if (autoScroll) term.scrollToBottom();
      saveTerminalContent(newId, terminalContentRef.current[newId]);
    });

    setTerminals((prev) => {
      const updatedTerminals = [...prev, terminalInstance];
      saveToLocalStorage(LOCAL_STORAGE_KEYS.TERMINALS, updatedTerminals.map(({ id, name }) => ({ id, name })));
      return updatedTerminals;
    });

    // Dispatch Redux actions for the new session
    dispatch(addSession(newId.toString())); // Add session to Redux store
    dispatch(setActiveSession(newId.toString())); // Set as active session

    setActiveTerminalId(newId);

    setTimeout(() => {
      if (terminalRefs.current[newId]) {
        term.open(terminalRefs.current[newId]!);
        fitAddon.fit();
        term.write(terminalContentRef.current[newId] || '');
      }
    }, 0);
  }, [dispatch, commands, onData, autoScroll, saveTerminalContent, terminals]);

  const closeTerminal = useCallback((id: number) => {
    dispatch(removeSession(id.toString())); // Remove session from Redux store

    setTerminals((prev) => {
      const updatedTerminals = prev.filter((term) => {
        if (term.id === id) {
          term.service.disconnect();
        }
        return term.id !== id;
      });
      saveToLocalStorage(LOCAL_STORAGE_KEYS.TERMINALS, updatedTerminals.map(({ id, name }) => ({ id, name })));
      return updatedTerminals;
    });

    if (activeTerminalId === id) {
      const remaining = terminals.filter((term) => term.id !== id);
      const nextId = remaining.length ? remaining[0].id : null;
      setActiveTerminalId(nextId);
      if (nextId) {
        dispatch(setActiveSession(nextId.toString())); // Update active session in Redux
      }
    }
  }, [dispatch, activeTerminalId, terminals]);

  const handleResizing = useCallback((e: MouseEvent) => {
    if (isResizing && activeTerminalId) {
      const height = window.innerHeight - e.clientY;
      terminalRefs.current[activeTerminalId]?.parentElement?.style.setProperty('height', `${height}px`);
    }
  }, [isResizing, activeTerminalId]);

  const handleResizeStart = (e: React.MouseEvent) => {
    e.preventDefault();
    setIsResizing(true);
    document.addEventListener('mousemove', handleResizing);
    document.addEventListener('mouseup', handleResizeEnd, { once: true });
  };

  const handleResizeEnd = () => {
    setIsResizing(false);
    document.removeEventListener('mousemove', handleResizing);
  };

  const scrollToBottom = () => {
    terminals.find((term) => term.id === activeTerminalId)?.xterm.scrollToBottom();
  };

  const toggleAutoScroll = () => setAutoScroll((prev) => !prev);

  useEffect(() => {
    saveToLocalStorage(LOCAL_STORAGE_KEYS.ACTIVE_TAB, activeTab);
  }, [activeTab]);

  useEffect(() => {
    saveToLocalStorage(LOCAL_STORAGE_KEYS.AUTO_SCROLL, autoScroll);
  }, [autoScroll]);

  useEffect(() => {
    terminalContentRef.current = loadFromLocalStorage(LOCAL_STORAGE_KEYS.TERMINAL_CONTENT) || {};
    const savedTerminals = loadFromLocalStorage(LOCAL_STORAGE_KEYS.TERMINALS);
    if (savedTerminals) {
      savedTerminals.forEach(() => createTerminal());
    }

    const savedActiveTab = loadFromLocalStorage(LOCAL_STORAGE_KEYS.ACTIVE_TAB);
    if (savedActiveTab) setActiveTab(savedActiveTab);

    const savedAutoScroll = loadFromLocalStorage(LOCAL_STORAGE_KEYS.AUTO_SCROLL);
    if (savedAutoScroll !== null) setAutoScroll(savedAutoScroll);

    if (terminals.length === 0) createTerminal();
  }, [createTerminal]);

  useImperativeHandle(ref, () => ({
    clearTerminal: () => {
      const activeTerminal = terminals.find((term) => term.id === activeTerminalId);
      activeTerminal?.xterm.clear();
      terminalContentRef.current[activeTerminalId!] = '';
      saveToLocalStorage(LOCAL_STORAGE_KEYS.TERMINAL_CONTENT, terminalContentRef.current);
    },
    writeToTerminal: (text: string) => {
      const activeTerminal = terminals.find((term) => term.id === activeTerminalId);
      if (activeTerminal) {
        activeTerminal.xterm.write(text);
        terminalContentRef.current[activeTerminalId!] += text;
        saveToLocalStorage(LOCAL_STORAGE_KEYS.TERMINAL_CONTENT, terminalContentRef.current);
      }
    },
  }));

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
        return <TerminalBody><p>🚨 Error: Cannot find module 'express' in /src/server.ts</p></TerminalBody>;
      case 'OUTPUT':
        return <TerminalBody><p>Build started...</p><p>Build succeeded. Serving on localhost:3000</p></TerminalBody>;
      case 'DEBUG_CONSOLE':
        return <TerminalBody><p>Debug initialized.</p><p>Breakpoint set in /src/utils.ts at line 42</p></TerminalBody>;
      default:
        return null;
    }
  };

  return (
    <TerminalContainer>
      <TerminalHeader>
        {['PROBLEMS', 'OUTPUT', 'DEBUG_CONSOLE', 'TERMINAL'].map((label) => (
          <TerminalTab key={label} $active={activeTab === label} onClick={() => setActiveTab(label as any)}>
            {label}
          </TerminalTab>
        ))}

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
          <ToolbarButton onClick={toggleAutoScroll} title={`Auto-scroll: ${autoScroll ? 'On' : 'Off'}`} $active={autoScroll}>
            <AiOutlineSync />
          </ToolbarButton>
        </Toolbar>
      </TerminalHeader>

      <div style={{ display: 'flex', height: '100%' }}>
        <TerminalsSidebar>
          {terminals.map((term) => (
            <SidebarTerminalItem
              key={term.id}
              $active={term.id === activeTerminalId}
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
