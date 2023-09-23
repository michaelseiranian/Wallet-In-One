import React from 'react';
import { render, fireEvent } from '@testing-library/react-native';
import DeveloperInfoScreen from '../../screens/pre_logged_in/DeveloperInfoScreen';
import { Linking } from 'react-native';
import renderer from 'react-test-renderer';

describe('<DeveloperInfoScreen />', () => {
    it('back to about us button test', () => {
        const navigate = jest.fn();
        const { getByText } = render(<DeveloperInfoScreen  navigation={{ navigate }}/>);
        fireEvent.press(getByText('Back to About Us'));
        expect(navigate).toHaveBeenCalledWith('About Us');
    })

    it('github button test krishna', () => {
        const github = jest.spyOn(Linking, 'openURL');
        const { getByTestId } = render(<DeveloperInfoScreen/>);
        fireEvent.press(getByTestId('GithubButtonTestKrishna'));
        expect(github).toHaveBeenCalledWith('https://github.com/krishnapk7');
    })

    it('github button test abbas', () => {
        const github = jest.spyOn(Linking, 'openURL');
        const { getByTestId } = render(<DeveloperInfoScreen/>);
        fireEvent.press(getByTestId('GithubButtonTestAbbas'));
        expect(github).toHaveBeenCalledWith('https://github.com/AbbasBinVakas');
    })

    it('github button test yusuf', () => {
        const github = jest.spyOn(Linking, 'openURL');
        const { getByTestId } = render(<DeveloperInfoScreen/>);
        fireEvent.press(getByTestId('GithubButtonTestYusuf'));
        expect(github).toHaveBeenCalledWith('https://github.com/YusufKCL');
    })

    it('github button test ezat', () => {
        const github = jest.spyOn(Linking, 'openURL');
        const { getByTestId } = render(<DeveloperInfoScreen/>);
        fireEvent.press(getByTestId('GithubButtonTestEzat'));
        expect(github).toHaveBeenCalledWith('https://github.com/XEZ1');
    })

    it('github button test shozab', () => {
        const github = jest.spyOn(Linking, 'openURL');
        const { getByTestId } = render(<DeveloperInfoScreen/>);
        fireEvent.press(getByTestId('GithubButtonTestShozab'));
        expect(github).toHaveBeenCalledWith('https://github.com/Shozab-N18');
    })

    it('github button test jamal', () => {
        const github = jest.spyOn(Linking, 'openURL');
        const { getByTestId } = render(<DeveloperInfoScreen/>);
        fireEvent.press(getByTestId('GithubButtonTestJamal'));
        expect(github).toHaveBeenCalledWith('https://github.com/JamalBoustani');
    })

    it('github button test michael', () => {
        const github = jest.spyOn(Linking, 'openURL');
        const { getByTestId } = render(<DeveloperInfoScreen/>);
        fireEvent.press(getByTestId('GithubButtonTestMichael'));
        expect(github).toHaveBeenCalledWith('https://github.com/mohawk49');
    })

    it('github button test matushan', () => {
        const github = jest.spyOn(Linking, 'openURL');
        const { getByTestId } = render(<DeveloperInfoScreen/>);
        fireEvent.press(getByTestId('GithubButtonTestMatushan'));
        expect(github).toHaveBeenCalledWith('https://github.com/mrmatyog');
    })

    it('snapshot developerInfoScreen test', () => {
        const developerInfoScreen = renderer.create(<DeveloperInfoScreen />);
        expect(developerInfoScreen).toMatchSnapshot();         
      });
})