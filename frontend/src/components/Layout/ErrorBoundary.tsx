// src/components/Layout/ErrorBoundary.tsx
import React, { Component, ErrorInfo } from 'react';
import styled from 'styled-components';

const ErrorContainer = styled.div.attrs({
  className: 'p-4 rounded-lg m-4'
})`
  background-color: ${props => props.theme.colors.background.tertiary};
  border: 1px solid ${props => props.theme.colors.border};
`;

interface Props {
  children: React.ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Error:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <ErrorContainer>
          <h2 className="text-lg font-bold mb-2">Something went wrong</h2>
          <pre className="text-sm">{this.state.error?.message}</pre>
        </ErrorContainer>
      );
    }

    return this.props.children;
  }
}