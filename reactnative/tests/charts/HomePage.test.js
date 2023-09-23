import React from 'react';
import { render, screen, fireEvent, act, waitFor} from '@testing-library/react-native';
import HomePage from '../../screens/charts/HomePage';
jest.useFakeTimers();
var data = {
    "Banks": [
        {
            "id": "6",
            "x": "HSBC Personal",
            "y": 9.98
        }
    ],
    "Cryptocurrency from exchanges": [
        {
            "id": 1,
            "x": "Binance",
            "y": 0.13
        }
    ],
    "Cryptocurrency from wallets": [
        {
            "id": 5,
            "x": "BTC Wallet: 3FZbgi29cpjq2Gj...",
            "y": 170.35
        }
    ],
    "Stock Accounts": [
        {
            "id": "xzaDvNRVJmcqe9BqLjGxH33o6oVye6hyy3lNK",
            "x": "Plaid IRA-Vanguard",
            "y": 266.23
        }
    ],
    "all": [
        {
            "x": "Banks",
            "y": 9.98
        },
        {
            "x": "Cryptocurrency from wallets",
            "y": 170.28
        },
        {
            "x": "Stock Accounts",
            "y": 266.23
        },
        {
            "x": "Cryptocurrency from exchanges",
            "y": 0.13
        }
    ]
}

describe('<HomePage />', () => {

    beforeEach(() => {
        global.fetch =  jest.fn( async () => {
            return Promise.resolve({
                status: 200, json: () => data
            })
        })
      })

      afterEach(() => {
        global.fetch.mockClear();
        delete global.fetch;
      })

    it('homePage pie chart bar chart test', async () => {
        const homePage = render(<HomePage/>);
        await act( async () => {
        await waitFor( () => {
            const activityIndicator = screen.UNSAFE_queryByType('ActivityIndicator');
            expect(activityIndicator).toBeNull();
        })
        fireEvent.press(await screen.getByTestId("stacked"))
        fireEvent.press(await screen.getByTestId("pie"))
        expect(homePage).toMatchSnapshot();
        })
    })

    it('homepage stacked bar chart test', async () => {
        const homePage = render(<HomePage/>);
        await act( async () => {
            await waitFor( () => {
                const activityIndicator = screen.UNSAFE_queryByType('ActivityIndicator');
                expect(activityIndicator).toBeNull();
            })
            fireEvent.press(await screen.getByTestId("stacked"))
            expect(homePage).toMatchSnapshot();
        })
    })
})

var emptyData = {"all": []}
describe('<HomePage /> No Data', () => {

    beforeEach(() => {
        global.fetch =  jest.fn( async () => {
            return Promise.resolve({
                status: 200, json: () => emptyData
            })
        })
      })

      afterEach(() => {
        global.fetch.mockClear();
        delete global.fetch;
      })

    
    it('homepage noData test', async () => {
        const homePage = render(<HomePage/>)
        await act( async () => {
            await waitFor( () => {
                const activityIndicator = screen.UNSAFE_queryByType('ActivityIndicator');
                expect(activityIndicator).toBeNull();
            })
            expect(homePage).toMatchSnapshot();
        })
    })
})