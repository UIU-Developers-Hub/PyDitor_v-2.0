// src/components/ActivityBar/index.tsx
import styled from 'styled-components';

const ActivityBarContainer = styled.div`
  background-color: ${props => props.theme.colors.activityBar};
  padding: ${props => props.theme.spacing.medium};
`;

const ActivityBarContent = styled.div`
  color: ${props => props.theme.colors.foreground.primary};
  background: ${props => props.theme.colors.background.primary};
`;

// Use the component in your JSX
const ActivityBar: React.FC = () => (
  <ActivityBarContainer>
    <ActivityBarContent>Activity Content</ActivityBarContent>
  </ActivityBarContainer>
);

export default ActivityBar;
