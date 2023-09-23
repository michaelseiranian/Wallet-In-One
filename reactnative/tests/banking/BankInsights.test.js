import React from 'react';
import { render, screen, fireEvent, act, within, waitFor} from '@testing-library/react-native';
import BankInsights from '../../screens/banking/BankInsights'
import testData from './fixtures/metrics.json'

global.fetch =  jest.fn( async (api, data ) => {
    return Promise.resolve({
        status: 200, json: () => testData
    })

})

describe('<BankInsights />', () => {
    it('snapshot test', async () => {
        

        const snapshot = render(<BankInsights/>);

        await act( async () => {
            
            await waitFor( () => {
                const activityIndicator = screen.UNSAFE_queryByType('ActivityIndicator');
                expect(activityIndicator).toBeNull();
            })

            // Test buttons can be pressed
            fireEvent.press(await screen.getByText('1 Month'));
            fireEvent.press(await screen.getByText('3 Month'));
            fireEvent.press(await screen.getByText('6 Month'));
            fireEvent.press(await screen.getByText('All'));

            fireEvent.press(await screen.getByText('Income'));
            fireEvent.press(await screen.getByText('Spending'));
            fireEvent.press(await screen.getByText('Both'));

        });

        expect(snapshot).toMatchSnapshot();
    }
    )
});