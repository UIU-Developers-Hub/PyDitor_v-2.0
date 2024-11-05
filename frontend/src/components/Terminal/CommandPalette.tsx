// src/components/Terminal/CommandPalette.tsx
import React, { useState, useEffect, useCallback } from 'react';
import styled from 'styled-components';

type Command = {
  name: string;
  action: () => void;
};

interface CommandPaletteProps {
  commands: Command[];
  isVisible: boolean;
  onClose: () => void;
}

const CommandPalette: React.FC<CommandPaletteProps> = ({ commands, isVisible, onClose }) => {
  const [query, setQuery] = useState('');
  const [filteredCommands, setFilteredCommands] = useState<Command[]>(commands);
  const [selectedIndex, setSelectedIndex] = useState(0);

  useEffect(() => {
    setFilteredCommands(
      commands.filter((command) =>
        command.name.toLowerCase().includes(query.toLowerCase())
      )
    );
  }, [query, commands]);

  const handleCommandClick = (action: () => void) => {
    action();
    onClose();
  };

  const handleKeyDown = useCallback((e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Escape') {
      onClose();
    } else if (e.key === 'ArrowDown') {
      setSelectedIndex((prevIndex) => (prevIndex + 1) % filteredCommands.length);
    } else if (e.key === 'ArrowUp') {
      setSelectedIndex((prevIndex) =>
        (prevIndex - 1 + filteredCommands.length) % filteredCommands.length
      );
    } else if (e.key === 'Enter' && filteredCommands[selectedIndex]) {
      handleCommandClick(filteredCommands[selectedIndex].action);
    }
  }, [filteredCommands, selectedIndex, onClose]);

  if (!isVisible) return null;

  return (
    <Overlay>
      <Modal>
        <Input
          type="text"
          placeholder="Type a command..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={handleKeyDown}
          autoFocus
        />
        <CommandList>
          {filteredCommands.map((command, index) => (
            <CommandItem
              key={index}
              onClick={() => handleCommandClick(command.action)}
              isSelected={index === selectedIndex}
            >
              {command.name}
            </CommandItem>
          ))}
        </CommandList>
      </Modal>
    </Overlay>
  );
};

// Styled Components
const Overlay = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
`;

const Modal = styled.div`
  background-color: #333;
  color: #fff;
  padding: 20px;
  border-radius: 8px;
  width: 400px;
  max-height: 60vh;
  overflow-y: auto;
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.2);
`;

const Input = styled.input`
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
  font-size: 16px;
  border-radius: 4px;
  border: none;
  outline: none;
`;

const CommandList = styled.ul`
  list-style: none;
  padding: 0;
  margin: 0;
`;

const CommandItem = styled.li<{ isSelected: boolean }>`
  padding: 10px;
  cursor: pointer;
  border-radius: 4px;
  margin-bottom: 5px;
  background-color: ${(props) => (props.isSelected ? '#555' : '#444')};
  color: ${(props) => (props.isSelected ? '#fff' : '#ddd')};

  &:hover {
    background-color: #555;
  }
`;

export default CommandPalette;
