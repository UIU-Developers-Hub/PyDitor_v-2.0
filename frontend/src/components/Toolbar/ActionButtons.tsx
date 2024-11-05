// src/components/Toolbar/ActionButtons.tsx
import React from 'react';
import styled from 'styled-components';
import { Save, Play, Settings } from 'lucide-react';

const ButtonContainer = styled.div`
  display: flex;
  gap: 0.5rem;
`;

const ActionButton = styled.button`
  padding: 0.5rem;
  color: ${props => props.theme.colors.foreground.secondary};
  border-radius: 0.25rem;

  &:hover {
    background-color: ${props => props.theme.colors.accent};
    color: ${props => props.theme.colors.foreground.primary};
  }
`;

export const ActionButtons: React.FC = () => {
  return (
    <ButtonContainer>
      <ActionButton>
        <Save size={16} />
      </ActionButton>
      <ActionButton>
        <Play size={16} />
      </ActionButton>
      <ActionButton>
        <Settings size={16} />
      </ActionButton>
    </ButtonContainer>
  );
};