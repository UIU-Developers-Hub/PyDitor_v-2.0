// src/components/CommandPalette/index.tsx
import React, { useState } from 'react';
import styled from 'styled-components';
import { Command } from 'cmdk';

const PaletteOverlay = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding-top: 20vh;
  z-index: 1000;
`;

const PaletteContainer = styled(Command)`
  width: 560px;
  max-width: 100%;
  background: ${props => props.theme.colors.background.secondary};
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 16px 32px rgba(0, 0, 0, 0.25);

  .cmdk-input {
    padding: 12px 16px;
    font-size: 16px;
    border: none;
    width: 100%;
    background: transparent;
    color: ${props => props.theme.colors.foreground.primary};
    outline: none;
    border-bottom: 1px solid ${props => props.theme.colors.border};
  }

  .cmdk-list {
    max-height: 400px;
    overflow: auto;
    padding: 8px;
  }

  .cmdk-item {
    padding: 8px 12px;
    border-radius: 4px;
    cursor: pointer;
    color: ${props => props.theme.colors.foreground.primary};
    display: flex;
    align-items: center;
    gap: 8px;

    &[data-selected="true"] {
      background: ${props => props.theme.colors.accent};
    }
  }
`;

interface CommandPaletteProps {
  isOpen: boolean;
  onClose: () => void;
  onCommand: (command: string) => void;
}

export const CommandPalette: React.FC<CommandPaletteProps> = ({
  isOpen,
  onClose,
  onCommand
}) => {
  const [search, setSearch] = useState('');

  if (!isOpen) return null;

  return (
    <PaletteOverlay onClick={onClose}>
      <PaletteContainer value={search} onValueChange={setSearch}>
        <input 
          className="cmdk-input"
          placeholder="Type a command or search..."
          autoFocus
          onClick={e => e.stopPropagation()}
        />
        <Command.List>
          <Command.Item onSelect={() => onCommand('newFile')}>
            New File
          </Command.Item>
          <Command.Item onSelect={() => onCommand('find')}>
            Find in Files
          </Command.Item>
          {/* Add more commands */}
        </Command.List>
      </PaletteContainer>
    </PaletteOverlay>
  );
};