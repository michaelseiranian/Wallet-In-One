import React from 'react';
import SettingsPage from 'reactnative/screens/SettingsPage';
import renderer from 'react-test-renderer';
import { render, screen, fireEvent, act } from '@testing-library/react-native';
import { useTheme } from 'reactnative/src/theme/ThemeProvider';
import * as SecureStore from "expo-secure-store";
jest.mock("expo-secure-store");
jest.mock('reactnative/src/theme/ThemeProvider');

SecureStore.getItemAsync.mockReset();
useTheme.mockReturnValue({
  dark: false,
  colors: {
    text: '#000',
    background: '#fff',
    primary: '#0af',
  },
  setScheme: jest.fn(),
  update: jest.fn(),
});

jest.mock('react', () => {
  const ActualReact = jest.requireActual('react')
  return {
    ...ActualReact,
    useContext: () => (ActualReact.useState({ 'signedIn': false })),
  }
})

it('snapshot test for settings page', () => {
  const navigate = jest.fn();
  const settingsPage = renderer.create(<SettingsPage navigation={{ navigate }} />);
  expect(settingsPage).toMatchSnapshot();
});

it('settings page pressing log out button test', () => {
  const navigate = jest.fn();
  const settingsPage = render(<SettingsPage navigation={{ navigate }} />);
  act(() => {
    fireEvent.press(screen.getByText('Logout'));
  });
  expect(settingsPage).toMatchSnapshot();
});


it('setting page dark mode toggle', () => {
  const navigate = jest.fn();
  const settingsPage = render(<SettingsPage navigation={{ navigate }} />);
  fireEvent.press(screen.getByText('Dark Mode'));
  expect(settingsPage).toMatchSnapshot();
});

it('setting page system default toggle', () => {
  const navigate = jest.fn();
  const settingsPage = render(<SettingsPage navigation={{ navigate }} />);
  fireEvent.press(screen.getByText('System Default'));
  expect(settingsPage).toMatchSnapshot();
});

it('setting page light mode toggle', () => {
  const navigate = jest.fn();
  const settingsPage = render(<SettingsPage navigation={{ navigate }} />);
  fireEvent.press(screen.getByText('Light Mode'));
  expect(settingsPage).toMatchSnapshot();
});