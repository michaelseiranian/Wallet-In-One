import { renderHook } from '@testing-library/react-hooks';
import useCryptoExchange from "../../screens/cryptoExchanges/useCryptoExchange";
import expect from "expect";
import {describe, test} from "@jest/globals";
import {act} from "@testing-library/react-native";


describe('useCryptoExchange', () => {
    test('should match snapshot', () => {
        const { result } = renderHook(() => useCryptoExchange());

        expect(result.current).toMatchSnapshot();
    });

    beforeEach(() => {
        jest.clearAllMocks();
    });

    test('fetchExchanges works correctly', async () => {
        const mockFetch = jest.fn(() =>
            Promise.resolve({
                json: () => Promise.resolve([{ id: 1, name: 'Exchange 1' }]),
            })
        );
        global.fetch = mockFetch;

        const { result, waitForNextUpdate } = renderHook(() => useCryptoExchange());
        expect(result.current.exchanges).toEqual([]);
    await act( async () => {
        await result.current.fetchExchanges();

        expect(mockFetch).toHaveBeenCalledWith(expect.stringContaining(`/crypto-exchanges`), {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Token undefined`,
            },
        });
        expect(result.current.exchanges).toEqual([{ id: 1, name: 'Exchange 1' }]);
    });
    });

    test('fetchExchange rejects expectedly', async () => {
        const mockFetch = jest.fn(() => {
            return Promise.reject();
        })

        global.fetch = mockFetch;
        const {result} = renderHook(() => useCryptoExchange());

        await act(async () => {
            result.current.setExchanges([{id: 1, name: 'Exchange 1'}]);

            await result.current.fetchExchanges();
        });
        expect(mockFetch).toHaveBeenCalledWith(expect.stringContaining(`/crypto-exchanges`), {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Token undefined`,
            }
        });
    });

    test('removeExchange works correctly', async () => {
            const mockFetch = jest.fn(() =>
                Promise.resolve({
                    json: () => Promise.resolve([{id: 1, name: 'Exchange 1'}, {id: 2, name: 'Exchange 2'}]),
                })
            );
            global.fetch = mockFetch;
            const {result} = renderHook(() => useCryptoExchange());


        await act(async () => {

            await result.current.setExchanges([{id: 1, name: 'Exchange 1'}, {id: 2, name: 'Exchange 2'}]);
            await result.current.removeExchange(1);

            expect(mockFetch).toHaveBeenCalledWith(expect.stringContaining(`/crypto-exchanges`), {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Token undefined`,
                },
                body: JSON.stringify({
                    id: 1,
                }),
            });
            expect(result.current.exchanges).toEqual([{id: 2, name: 'Exchange 2'}]);
        });

    });

    test('removeExchange rejects expectedly', async () => {
        const mockFetch = jest.fn(() => {
            return Promise.reject();
        })

        global.fetch = mockFetch;
        const {result} = renderHook(() => useCryptoExchange());

        await act(async () => {
            result.current.setExchanges([{use: 1, name: 'Exchange 1'}]);

            await result.current.removeExchange(1);
        });
            expect(mockFetch).toHaveBeenCalledWith(expect.stringContaining(`/crypto-exchanges`), {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Token undefined`,
                },
                body: JSON.stringify({
                    id: 1,
                }),
            });
    });


});