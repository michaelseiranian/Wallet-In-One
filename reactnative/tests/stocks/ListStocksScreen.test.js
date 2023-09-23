import React from "react";
import { render, screen, fireEvent, act, waitFor} from '@testing-library/react-native';
import SuccessComponent from "../../screens/stocks/ListStocksScreen";
import stocks from './fixtures/stocks.json'
import transactions from './fixtures/transaction.json'

var navigationData = {
    "accessToken": "access-sandbox-9cf73c44-d4f5-4a9c-84ce-6203d35aa40d",
    "accountID": "ALxMKPjkkdtZVpLBdXx8ia9prXRBmwh67wXWd",
    "account_name": "Plaid IRA",
    "balance": "266.23",
    "balance_currency": "GBP",
    "logo": "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",
    "name": "Vanguard",
    "transactions": undefined
}

/**
 * Tests for the ListStocksScreen
 */
describe('<SuccessComponent />', () => {

    beforeEach(() => {
        global.fetch =  jest.fn( async (url) => {
            if(url.includes('list_accounts')){
            return Promise.resolve({
                status: 200, json: () => stocks.all
            })
            }
            else{
                return Promise.resolve({
                    status: 200, json: () => transactions.all
                })
            }
        })
      })

      afterEach(() => {
        global.fetch.mockClear();
        delete global.fetch;
      })

      it('listStocksScreen snapshot test', async () => {
        const listStocksScreen = render(<SuccessComponent />);

            await waitFor( () => {
                const loading = screen.UNSAFE_queryByType('ActivityIndicator');
                expect(loading).toBeNull();
            })
        expect(listStocksScreen).toMatchSnapshot();
    }
    )

    it('listStocksScreen test touchable opacity', async () => {
        const navigate = jest.fn();
        const listStocksScreen = render(<SuccessComponent navigation={{ navigate }}/>);

            await waitFor( () => {
                const loading = screen.UNSAFE_queryByType('ActivityIndicator');
                expect(loading).toBeNull();
            })
        fireEvent.press(await screen.getByText('Plaid IRA'));
        expect(navigate).toHaveBeenCalledWith("StockAsset", navigationData);
    }
    )
})

describe('<SuccessComponent />', () => {
    beforeEach(() => {
        global.fetch =  jest.fn( async (url) => {
            return Promise.resolve({
                status: 200, json: () => null
            })
        })
      })

      afterEach(() => {
        global.fetch.mockClear();
        delete global.fetch;
      })

      it('listStocksScreen empty data', async () => {
        const listStocksScreen = render(<SuccessComponent />);

        await waitFor( () => {
            const loading = screen.UNSAFE_queryByType('ActivityIndicator');
            expect(loading).toBeNull();
        })
        expect(listStocksScreen).toMatchSnapshot();
      })
})