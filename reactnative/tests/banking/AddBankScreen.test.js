import React from 'react';
import { render, screen, fireEvent, act, within, waitFor} from '@testing-library/react-native';
import AddBankScreen from '../../screens/banking/AddBankScreen'
import bank_list from './fixtures/bank_list.json'

global.fetch =  jest.fn( async (api, data ) => {
    const url = {"url": "https://ob.nordigen.com/psd2/start/d351dc6a-408a-4a68-8762-34a0346eca9a/AIRWALLEX_AIPTAU32"}
    if (api.includes("AIRWALLEX_AIPTAU32")){
        return Promise.resolve({ status: 200, json: () => url })
    }
    else { 
      return Promise.resolve({ status: 200, json: () => bank_list})
    }
})

describe('<AddBankScreen />', () => {
    it('snapshot test', async () => {
        const snapshot = render(<AddBankScreen />);

        await act( async () => {
            
            await waitFor( () => {
                const activityIndicator = screen.UNSAFE_queryByType('ActivityIndicator');
                expect(activityIndicator).toBeNull();
            })
            fireEvent.press(await screen.getByText('Airwallex'));

            expect(snapshot).toMatchSnapshot();
        });
    }
    )
});