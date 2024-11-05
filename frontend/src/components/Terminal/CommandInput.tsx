// src/components/Terminal/CommandInput.tsx
import React, { useState } from 'react';
import styled from 'styled-components';

interface CommandInputProps {
  onSubmit: (command: string) => void;
  placeholder?: string;
}

const CommandInput: React.FC<CommandInputProps> = ({ onSubmit, placeholder = 'Type a command...' }) => {
  const [command, setCommand] = useState('');

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      onSubmit(command);
      setCommand('');
    }
  };

  return (
    <InputContainer>
      <StyledInput
        type="text"
        placeholder={placeholder}
        value={command}
        onChange={(e) => setCommand(e.target.value)}
        onKeyDown={handleKeyDown}
      />
      {command && (
        <ClearButton onClick={() => setCommand('')} title="Clear">
          ✖
        </ClearButton>
      )}
    </InputContainer>
  );
};

// Styled Components
const InputContainer = styled.div`
  display: flex;
  align-items: center;
  width: 100%;
`;

const StyledInput = styled.input`
  width: 100%;
  padding: 8px;
  border: none;
  border-top: 1px solid ${(props) => props.theme.colors.border};
  background: ${(props) => props.theme.colors.background.primary};
  color: ${(props) => props.theme.colors.foreground.primary};
  font-family: ${(props) => props.theme.typography.fontFamily};
  font-size: ${(props) => props.theme.typography.fontSize};
  outline: none;
`;

const ClearButton = styled.button`
  background: transparent;
  border: none;
  color: #888;
  cursor: pointer;
  font-size: 18px;
  padding: 0 8px;
`;

export default CommandInput;
