import { renderHook } from '@testing-library/react-hooks';
import useCryptoExchangeBalances from "../../screens/cryptoExchanges/useCryptoExchangeBalances";
import expect from "expect";
import {describe, test} from "@jest/globals";
import {act} from "@testing-library/react-native";
import useCryptoExchange from "../../screens/cryptoExchanges/useCryptoExchange";


describe('useCryptoExchangeBalances', () => {
    test('should match snapshot', () => {
        const { result } = renderHook(() => useCryptoExchangeBalances());
        expect(result.current).toMatchSnapshot();
    });

    beforeEach(() => {
        jest.clearAllMocks();
    });

    test('fetchBalances works correctly', async () => {
        const mockFetch = jest.fn(() =>
            Promise.resolve({
                json: () => Promise.resolve([
                    {
                        "x": "Binance",
                        "y": 500,
                        "id": 1
                    }
                ]),
            })
        );
        global.fetch = mockFetch;

        const { result } = renderHook(() => useCryptoExchangeBalances());
        expect(result.current.balances).toEqual([]);
        await act( async () => {
            await result.current.fetchBalances();

            expect(mockFetch).toHaveBeenCalledWith(expect.stringContaining(`/crypto-exchanges/get_exchange_balances/`), {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Token undefined`,
                },
            });
            expect(result.current.balances).toEqual([
                {
                    "x": "Binance",
                    "y": 500,
                    "id": 1
                }
            ]);
        });
    });

    test('fetchBalances rejects expectedly', async () => {
        const mockFetch = jest.fn(() => {
            return Promise.reject();
        })

        global.fetch = mockFetch;
        const {result} = renderHook(() => useCryptoExchangeBalances());

        await act(async () => {
            result.current.setBalances([{"x": "Binance", "y": 500, "id": 1}]);

            await result.current.fetchBalances();
        });
        expect(mockFetch).toHaveBeenCalledWith(expect.stringContaining(`/crypto-exchanges/get_exchange_balances/`), {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Token undefined`,
            }
        });
    });
});