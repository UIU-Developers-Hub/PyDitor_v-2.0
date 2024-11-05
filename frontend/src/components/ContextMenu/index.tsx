// src/components/ContextMenu/index.tsx
import React, { useEffect } from 'react';
import styled from 'styled-components';

interface MenuItem {
  label?: string;
  action?: () => void;
  type?: 'separator';
}

interface ContextMenuProps {
  x: number;
  y: number;
  items: MenuItem[];
  onClose: () => void;
}

const MenuContainer = styled.div`
  position: fixed;
  background: ${props => props.theme.colors.background.secondary};
  border: 1px solid ${props => props.theme.colors.border};
  border-radius: 4px;
  padding: 4px 0;
  min-width: 160px;
  z-index: 1000;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
`;

const MenuItem = styled.div`
  padding: 6px 12px;
  cursor: pointer;
  color: ${props => props.theme.colors.foreground.primary};

  &:hover {
    background: ${props => props.theme.colors.selection};
  }
`;

const Separator = styled.div`
  height: 1px;
  background: ${props => props.theme.colors.border};
  margin: 4px 0;
`;

export const ContextMenu: React.FC<ContextMenuProps> = ({
  x,
  y,
  items,
  onClose
}) => {
  useEffect(() => {
    const handleClick = () => onClose();
    window.addEventListener('click', handleClick);
    return () => window.removeEventListener('click', handleClick);
  }, [onClose]);

  return (
    <MenuContainer style={{ left: x, top: y }}>
      {items.map((item, index) => (
        item.type === 'separator' ? (
          <Separator key={index} />
        ) : (
          <MenuItem
            key={index}
            onClick={(e) => {
              e.stopPropagation();
              item.action?.();
              onClose();
            }}
          >
            {item.label}
          </MenuItem>
        )
      ))}
    </MenuContainer>
  );
};