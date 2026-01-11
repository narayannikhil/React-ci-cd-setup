// src/__tests__/App.test.jsx
import { render, screen, fireEvent } from '@testing-library/react';
import { describe, expect, test } from 'vitest';
import App from '../App';
// Remove the CSS import - tests don't need it!

describe('App Component', () => {
  test('renders Vite + React text', () => {
    render(<App />);
    const headerElement = screen.getByText(/Vite \+ React/i);
    expect(headerElement).toBeInTheDocument();
  });

  test('increments count on button click', () => {
    render(<App />);
    
    const buttonElement = screen.getByText(/count is 0/i);
    expect(buttonElement).toBeInTheDocument();
    
    fireEvent.click(buttonElement);
    expect(buttonElement).toHaveTextContent('count is 1');
    
    fireEvent.click(buttonElement);
    expect(buttonElement).toHaveTextContent('count is 2');
  });
});