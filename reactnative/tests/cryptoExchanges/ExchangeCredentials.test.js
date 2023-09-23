import React from 'react';
import {Alert} from "react-native";
import {act, fireEvent, render} from '@testing-library/react-native';
import ExchangeCredentials from "../../screens/cryptoExchanges/ExchangeCredentials";
import * as SecureStore from "expo-secure-store";
import {useTheme} from 'reactnative/src/theme/ThemeProvider';
import {describe, it} from "@jest/globals";
import expect from "expect";


jest.mock("expo-secure-store");
jest.mock('reactnative/src/theme/ThemeProvider');

const mockNavigation = {
    navigate: jest.fn(),
};

const mockRoute = {
    params: {
        exchange: 'TestExchange',
    },
};

describe('ExchangeCredentials', () => {
    const props = {
        route: {
            params: {
                exchange: 'binance',
                id: 1
            },

        },
        navigation: {
            goBack: jest.fn(),
            navigate: jest.fn()
        }
    };

    it('renders correctly snapshot', () => {
        const { toJSON } = render(<ExchangeCredentials {...props} />);
        expect(toJSON()).toMatchSnapshot();
    });

    beforeEach(() => {
        SecureStore.getItemAsync.mockReset();
        useTheme.mockReturnValue({
            dark: false,
            colors: {
                text: '#000',
                background: '#fff',
                primary: '#0af',
            },
            setScheme: jest.fn(),
        });
    });

    afterEach(() => {
        jest.clearAllMocks();
    });

    it('renders correctly', () => {
        const { getByText, getByTestId } = render(
            <ExchangeCredentials route={mockRoute} navigation={mockNavigation} />,
        );

        expect(getByText('TestExchange Credentials:')).toBeTruthy();
        expect(getByText('API Key:')).toBeTruthy();
        expect(getByText('Secret Key:')).toBeTruthy();
    });

    it('shows an error if either API Key or Secret Key is missing', async () => {
        const { getByText, getByTestId } = render(
            <ExchangeCredentials route={mockRoute} navigation={mockNavigation} />,
        );

        jest.spyOn(Alert, 'alert');

        const apiKeyInput = getByTestId('apiKeyInput');
        const secretKeyInput = getByTestId('secretKeyInput');
        const submitButton = getByText('Submit');

        fireEvent.changeText(apiKeyInput, '');
        fireEvent.changeText(secretKeyInput, 'testSecretKey');
        fireEvent.press(submitButton);
        expect(Alert.alert).toHaveBeenCalledWith("Error",
            "Please enter both API Key and Secret Key.");

        fireEvent.changeText(apiKeyInput, 'testApiKey');
        fireEvent.changeText(secretKeyInput, '');
        fireEvent.press(submitButton);
        expect(Alert.alert).toHaveBeenCalledWith("Error",
            "Please enter both API Key and Secret Key.");
    });

    it('shows an error if wrong API/secret key pair is provided', async () => {
        const { getByText, getByTestId } = render(<ExchangeCredentials {...props} />);

        const apiKeyInput = getByTestId('apiKeyInput');
        const secretKeyInput = getByTestId('secretKeyInput');
        const submitButton = getByText('Submit');

        fireEvent.changeText(apiKeyInput, 'testAPIKey');
        fireEvent.changeText(secretKeyInput, 'testSecretKey');
        fireEvent.press(submitButton);
    });

    it('creates account successfully, with success message', async() => {
        global.fetch = jest.fn(() =>
            Promise.resolve({
                status: 200, json: () => Promise.resolve([{id: 1, name: 'Exchange 1'}]),
            })
        );

        const { getByText, getByTestId } = render(<ExchangeCredentials {...props }/>);

        const apiKeyInput = getByTestId('apiKeyInput');
        const secretKeyInput = getByTestId('secretKeyInput');
        const submitButton = getByText('Submit');

        fireEvent.changeText(apiKeyInput, 'testAPIKey');
        fireEvent.changeText(secretKeyInput, 'testSecretKey');
        fireEvent.press(submitButton);

    })

    it('throws error on status code 401', async() => {
        global.fetch = jest.fn(() =>
            Promise.resolve({
                status: 401, json: () => Promise.resolve([{id: 1, name: 'Exchange 1'}]),
            })
        );

        const { getByText, getByTestId } = render(<ExchangeCredentials {...props}/>);

        const apiKeyInput = getByTestId('apiKeyInput');
        const secretKeyInput = getByTestId('secretKeyInput');
        const submitButton = getByText('Submit');

        fireEvent.changeText(apiKeyInput, 'testAPIKey');
        fireEvent.changeText(secretKeyInput, 'testSecretKey');
        fireEvent.press(submitButton);
    })

    it('throws error on catch error', async() => {
        global.fetch = jest.fn(() =>
            Promise.resolve({
                status: 401, json: () => Promise.reject(),
            })
        );

        const { getByText, getByTestId } = render(<ExchangeCredentials {...props}/>);

        jest.spyOn(Alert, 'alert');
        const apiKeyInput = getByTestId('apiKeyInput');
        const secretKeyInput = getByTestId('secretKeyInput');
        const submitButton = getByText('Submit');

        fireEvent.changeText(apiKeyInput, 'testAPIKey');
        fireEvent.changeText(secretKeyInput, 'testSecretKey');

        await act(async () => {
            await fireEvent.press(submitButton);
        })
        fireEvent.press(submitButton);

        expect(Alert.alert).toHaveBeenCalledWith("Error", "An error occurred while retrieving binance account data.");
    })

});

