import React from 'react';
import { render, fireEvent } from '@testing-library/react-native';
import AboutUsScreen from '../../screens/pre_logged_in/AboutUsScreen';
import renderer from 'react-test-renderer';

describe('<AboutUsScreen/>', () => {
    it('developer team button test', () => {
        const navigate = jest.fn();
        const { getByText } = render(<AboutUsScreen  navigation={{ navigate }}/>);
        fireEvent.press(getByText('Meet the team!'));
        expect(navigate).toHaveBeenCalledWith('Developer Info');
    })

    it('start button test', () => {
        const navigate = jest.fn();
        const { getByText } = render(<AboutUsScreen  navigation={{ navigate }}/>);
        fireEvent.press(getByText('Home Page'));
        expect(navigate).toHaveBeenCalledWith('Start');
    })

    it('snapshot aboutUsScreen test', () => {
        const navigate = jest.fn();
        const aboutUsScreen = renderer.create(<AboutUsScreen navigation={{ navigate }} />);
        expect(aboutUsScreen).toMatchSnapshot();         
      });
})