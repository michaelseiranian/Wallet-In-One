import React from 'react';
import { render, screen, fireEvent, act, within, waitFor} from '@testing-library/react-native';
import BankTransactionsScreen from '../../screens/banking/BankTransactionsScreen'
import { useTheme } from 'reactnative/src/theme/ThemeProvider';
import * as SecureStore from "expo-secure-store";

jest.mock("expo-secure-store");
jest.mock('reactnative/src/theme/ThemeProvider');

SecureStore.getItemAsync.mockReset();

global.fetch =  jest.fn( async (api, data ) => {

    const transactions = [{
        "id": "abc",
        "time": "2023-03-12T11:42:32Z",
        "amount_currency": "GBP",
        "amount": "-10.00",
        "info": "t1",
        "account": "def",
        "formatted_amount": {
            "string": "-£10.00",
            "currency": "GBP",
            "amount": "-10.00"
        }
    },
    {
        "id": "def",
        "time": "2023-03-11T11:46:36Z",
        "amount_currency": "GBP",
        "amount": "5.00",
        "info": "t2",
        "account": "def",
        "formatted_amount": {
            "string": "£5.00",
            "currency": "GBP",
            "amount": "5.00"
        }
    }]

    function hasAccountID(url) {
        const pattern = /\/transactions\/[^/]+(\/|$)/;
        return pattern.test(url);
    }
    if (hasAccountID(api)){
        return Promise.resolve({
            status: 200, json: () => [transactions[1]]
        })
    }
    else{
        return Promise.resolve({
            status: 200, json: () => transactions
        })
    }

})

describe('<BankTransactionsScreen />', () => {
    it('test transactions with multiple accounts', async () => {
        
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

        const snapshot = render(<BankTransactionsScreen route={{params: undefined}}/>);

        await act( async () => {
            
            await waitFor( () => {
                const activityIndicator = screen.UNSAFE_queryByType('ActivityIndicator');
                expect(activityIndicator).toBeNull();
            })

        });

        expect(screen.queryAllByText('t1')).toHaveLength(1)
        expect(screen.queryAllByText('-£10.00')).toHaveLength(1)
        expect(screen.queryAllByText('t2')).toHaveLength(1)
        expect(screen.queryAllByText('£5.00')).toHaveLength(1)


    }
    )

    it('test transactions with 1 account', async () => {

        useTheme.mockReturnValue({
            dark: true,
            colors: {
              text: '#000',
              background: '#fff',
              primary: '#0af',
            },
            setScheme: jest.fn(),
            update: jest.fn(),
          });

        const snapshot = render(<BankTransactionsScreen route={{params: 'abc'}}/>);

        await act( async () => {
            
            await waitFor( () => {
                const activityIndicator = screen.UNSAFE_queryByType('ActivityIndicator');
                expect(activityIndicator).toBeNull();
            })

        });

        expect(screen.queryAllByText('t1')).toHaveLength(0)
        expect(screen.queryAllByText('-£10.00')).toHaveLength(0)
        expect(screen.queryAllByText('t2')).toHaveLength(1)
        expect(screen.queryAllByText('£5.00')).toHaveLength(1)

    }
    )
});