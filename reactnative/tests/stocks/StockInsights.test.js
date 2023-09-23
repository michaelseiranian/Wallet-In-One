import React from 'react';
import { render, screen, fireEvent, act, waitFor} from '@testing-library/react-native';
import StockInsight from '../../screens/stocks/StocksInsightScreen';
import insights from './fixtures/insights.json'
import emptyInsights from './fixtures/emptyInsights.json'

/**
 * Tests for stock insights screen
 */
describe('<StockInsight />', () => {

    beforeEach(() => {
        global.fetch =  jest.fn( async () => {
            return Promise.resolve({
                status: 200, json: () => insights
            })
        })
      })

      afterEach(() => {
        global.fetch.mockClear();
        delete global.fetch;
      })

    it('stockInsight snapshot test', async () => {
        const stockInsight = render(<StockInsight/>);

            await waitFor( () => {
                const loading = screen.UNSAFE_queryByType('ActivityIndicator');
                expect(loading).toBeNull();
            })
        expect(stockInsight).toMatchSnapshot();
    }
    )

    it('test 1 month stock insight', async () => {

        const stockInsight = render(<StockInsight />);

        await act( async () => {
            
            await waitFor( () => {
                const activityIndicator = screen.UNSAFE_queryByType('ActivityIndicator');
                expect(activityIndicator).toBeNull();
            })

            fireEvent.press(await screen.getByTestId('1 Month'));
            expect(screen.getByText("Number of Transactions: 13"))
            expect(screen.getByText("Highest Transaction(£): 387.37"))
            expect(screen.getByText("Lowest Transaction(£): -12418.45"))
            expect(screen.getByText("Average Transaction(£): -1218.68"))
            expect(screen.getByText("Variance: 10783023.6"))
            expect(screen.getByText("Standard Deviation: 3283.75"))
            expect(screen.getByText("Highest Fee(£): 7.99"))
            expect(screen.getByText("Lowest Fee(£): 0"))
            expect(screen.getByText("Average Fee(£): 3.07"))
            expect(screen.UNSAFE_queryByType('Map')).toBeDefined()
        });
        expect(stockInsight).toMatchSnapshot();
    }
    )

    it('test 3 months stock insight', async () => {

        const stockInsight = render(<StockInsight/>);

        await act( async () => {
            
            await waitFor( () => {
                const activityIndicator = screen.UNSAFE_queryByType('ActivityIndicator');
                expect(activityIndicator).toBeNull();
            })

            fireEvent.press(await screen.getByTestId('3 Months'));
            expect(screen.getByText("Number of Transactions: 39"))
            expect(screen.getByText("Highest Transaction(£): 387.37"))
            expect(screen.getByText("Lowest Transaction(£): -12418.45"))
            expect(screen.getByText("Average Transaction(£): -1218.68"))
            expect(screen.getByText("Variance: 10783023.6"))
            expect(screen.getByText("Standard Deviation: 3283.75"))
            expect(screen.getByText("Highest Fee(£): 7.99"))
            expect(screen.getByText("Lowest Fee(£): 0"))
            expect(screen.getByText("Average Fee(£): 3.07"))
            expect(screen.UNSAFE_queryByType('Map')).toBeDefined()
        });
        expect(stockInsight).toMatchSnapshot();
    }
    )

    it('test 6 months stock insight', async () => {

        const stockInsight = render(<StockInsight/>);

        await act( async () => {
            
            await waitFor( () => {
                const activityIndicator = screen.UNSAFE_queryByType('ActivityIndicator');
                expect(activityIndicator).toBeNull();
            })

            fireEvent.press(await screen.getByTestId('6 Months'));
            expect(screen.getByText("Number of Transactions: 78"))
            expect(screen.getByText("Highest Transaction(£): 387.37"))
            expect(screen.getByText("Lowest Transaction(£): -12418.45"))
            expect(screen.getByText("Average Transaction(£): -1218.68"))
            expect(screen.getByText("Variance: 10783023.6"))
            expect(screen.getByText("Standard Deviation: 3283.75"))
            expect(screen.getByText("Highest Fee(£): 7.99"))
            expect(screen.getByText("Lowest Fee(£): 0"))
            expect(screen.getByText("Average Fee(£): 3.07"))
            expect(screen.UNSAFE_queryByType('Map')).toBeDefined()
        });
        expect(stockInsight).toMatchSnapshot();
    }
    )

    it('test 1 year stock insight', async () => {

        const stockInsight = render(<StockInsight/>);

        await act( async () => {
            
            await waitFor( () => {
                const activityIndicator = screen.UNSAFE_queryByType('ActivityIndicator');
                expect(activityIndicator).toBeNull();
            })

            fireEvent.press(await screen.getByTestId('1 Year'));
            expect(screen.getByText("Number of Transactions: 136"))
            expect(screen.getByText("Highest Transaction(£): 387.37"))
            expect(screen.getByText("Lowest Transaction(£): -12418.45"))
            expect(screen.getByText("Average Transaction(£): -1204.22"))
            expect(screen.getByText("Variance: 10334689.14"))
            expect(screen.getByText("Standard Deviation: 3214.76"))
            expect(screen.getByText("Highest Fee(£): 7.99"))
            expect(screen.getByText("Lowest Fee(£): 0"))
            expect(screen.getByText("Average Fee(£): 3.01"))
            expect(screen.UNSAFE_queryByType('Map')).toBeDefined()
        });
        expect(stockInsight).toMatchSnapshot();
    }
    )
});

describe('<StockInsight /> Empty Data', () => {
    beforeEach(() => {
        global.fetch =  jest.fn( async () => {
            return Promise.resolve({
                status: 200, json: () => emptyInsights
            })
        })
      })

      afterEach(() => {
        global.fetch.mockClear();
        delete global.fetch;
      })

      it('test empty insights', async () => {

        const stockInsight = render(<StockInsight/>);

        await act( async () => {
            
            await waitFor( () => {
                const activityIndicator = screen.UNSAFE_queryByType('ActivityIndicator');
                expect(activityIndicator).toBeNull();
            })

            expect(screen.getByText("No Data for Selected Date"))
        });
        expect(stockInsight).toMatchSnapshot();
    }
    )
});

describe('<StockInsight /> 400', () => {
    beforeEach(() => {
        global.fetch =  jest.fn( async () => {
            return Promise.resolve({
                status: 400
            })
        })
      })

      afterEach(() => {
        global.fetch.mockClear();
        delete global.fetch;
      })

      it('does not render', async () => {
        const stockInsight = render(<StockInsight/>);
        const text = screen.queryByText('No Data for Selected Date');
        expect(text).toBeNull();
      })
})