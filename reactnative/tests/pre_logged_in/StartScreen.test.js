import React from 'react';
import { render, fireEvent } from '@testing-library/react-native';
import StartScreen from '../../screens/pre_logged_in/StartScreen';
import renderer from 'react-test-renderer';

describe('<StartScreen />', () => {

    it('about us button test', () => {
        const navigate = jest.fn();
        const { getByText } = render(<StartScreen navigation={{ navigate }} />);
        fireEvent.press(getByText('About Us'));
        expect(navigate).toHaveBeenCalledWith('About Us');
    });

    it('sign up button test', () => {
        const navigate = jest.fn();
        const { getByText } = render(<StartScreen navigation={{ navigate }} />);
        fireEvent.press(getByText('Sign Up'));
        expect(navigate).toHaveBeenCalledWith('Sign Up');
    });

    it('login button test', () => {
        const navigate = jest.fn();
        const { getByText } = render(<StartScreen navigation={{ navigate }} />);
        fireEvent.press(getByText('Log In'));
        expect(navigate).toHaveBeenCalledWith('Login');
    });

    it('snapshot startScreen test', () => {
        const navigate = jest.fn();
        const startScreen = renderer.create(<StartScreen navigation={{ navigate }} />);
        expect(startScreen).toMatchSnapshot();         
      });
});