import React from 'react';
import { render, screen, fireEvent, act, waitFor} from '@testing-library/react-native';
import StockDetails from '../../screens/stocks/StockDetails';
import transactions from './fixtures/transactions.json';
import stocks from './fixtures/stocks.json'

/**
 * Tests for StockDetails Screen
 */
describe('<StockDetails />', () => {

    beforeEach(() => {
        global.fetch =  jest.fn( async () => {
            return Promise.resolve({
                status: 200, json: () => transactions.transactions
            })
        })
      })

      afterEach(() => {
        global.fetch.mockClear();
        delete global.fetch;
      })

    it('stockDetails snapshot test', async () => {
        const stockDetails = render(<StockDetails route={{params: {"stock": stocks.stock}}}/>);

        await act( async () => {
            await waitFor( () => {
                const loading = screen.queryByText('Loading...');
                expect(loading).toBeNull();
            })
        });
        expect(stockDetails).toMatchSnapshot();
    }
    )

    it('stockDetails name test', async () => {
        const stockDetails = render(<StockDetails route={{params: {"stock": stocks.stock}}}/>);
        await act( () => {
            expect(screen.getByText("Name"))
            expect(screen.getByText("Nflx Feb 01'18 $355 Call"))
        });
    }
    )

    it('stockDetails currency test', async () => {
        const stockDetails = render(<StockDetails route={{params: {"stock": stocks.stock}}}/>);
        await act( () => {
            expect(screen.getByText("Institution Price Currency"))
            expect(screen.getByText("GBP"))
        });
    }
    )

    it('stockDetails price test', async () => {
        const stockDetails = render(<StockDetails route={{params: {"stock": stocks.stock}}}/>);
        await act( () => {
            expect(screen.getByText("Institution Price"))
            expect(screen.getByText("1.00"))
        });
    }
    )

    it('stockDetails ticker symbol test', async () => {
        const stockDetails = render(<StockDetails route={{params: {"stock": stocks.stock}}}/>);
        await act( () => {
            expect(screen.getByText("Ticker Symbol"))
            expect(screen.getByText("NFLX180201C00355000"))
        });
    }
    )

    it('stockDetails quantity test', async () => {
        const stockDetails = render(<StockDetails route={{params: {"stock": stocks.stock}}}/>);
        await act( () => {
            expect(screen.getByText("Quantity"))
            expect(screen.getByText("0.01"))
        });
    }
    )
})