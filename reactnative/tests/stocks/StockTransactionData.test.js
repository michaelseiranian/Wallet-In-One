import React from 'react';
import { render, screen, waitFor} from '@testing-library/react-native';
import TransactionData from '../../screens/stocks/StockTransactionData';
import transaction from './fixtures/transaction.json';

/**
 * Tests for transaction data screen
 */
describe('<TransactionData />', () => {

    beforeEach(() => {
        global.fetch =  jest.fn( async (id) => {
            return Promise.resolve({
                status: 200, json: () => transaction
            })
        })
      })

      afterEach(() => {
        global.fetch.mockClear();
        delete global.fetch;
      })

    it('transactionData snapshot test', async () => {
        const transactionData = render(<TransactionData route={{params: "701"}} />);

        await waitFor( () => {
            const loading = screen.UNSAFE_queryByType('ActivityIndicator');
            expect(loading).toBeNull();
        })
        expect(transactionData).toMatchSnapshot();
    }
    )

    it('test transactionData fields', async () => {
        const transactionData = render(<TransactionData route={{params: "701"}} />);

        await waitFor( () => {
            const loading = screen.UNSAFE_queryByType('ActivityIndicator');
            expect(loading).toBeNull();
        })
        expect(screen.getByText("Name"))
        expect(screen.getByText("BUY NFLX DERIVATIVE"))
        expect(screen.getByText("Transaction ID"))
        expect(screen.getByText("WraX31pG9AuzLlKzAG8JIAAyNV9PZEuPaBq3k"))
        expect(screen.getByText("Amount"))
        expect(screen.getByText("£ 38.45"))
        expect(screen.getByText("Date"))
        expect(screen.getByText("2023-03-10"))
        expect(screen.getByText("Quantity"))
        expect(screen.getByText("4211.152345617756"))
        expect(screen.getByText("Price"))
        expect(screen.getByText("£ 0.01"))
        expect(screen.getByText("Fees"))
        expect(screen.getByText("£ 5"))
        expect(screen.UNSAFE_queryByType('Map')).toBeDefined()
    }
    )
});

describe('<TransactionData /> Incorrect ID', () => {
    beforeEach(() => {
        global.fetch =  jest.fn( async (id) => {
            return Promise.resolve({
                status: 400, json: () => null
            })
        })
      })

      afterEach(() => {
        global.fetch.mockClear();
        delete global.fetch;
      })

      it('test transactionData null', async () => {
        const transactionData = render(<TransactionData route={{params: "1"}} />);

        expect(screen.UNSAFE_queryByType('ActivityIndicator')).toBeDefined()
    }
    )
})
