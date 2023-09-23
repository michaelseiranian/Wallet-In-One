import AddStocksHelper from "../../screens/stocks/AddStocksHelper";
import {renderHook, act} from "@testing-library/react-native";
import transaction from "./fixtures/transaction.json"

/**
 * Tests for the AddStocksHelper custom react hook
 */
describe('<AddStocksHelper />', () => {

    afterEach(() => {
        global.fetch.mockClear();
        delete global.fetch;
    })

    it('test get access token', async () => {
        global.fetch =  jest.fn( async () => {
            return Promise.resolve({
              status: 200, json: () => ({access_token: 'access-sandbox-c314b575-cc3d-4897-ae93-c792eb4c2d7c'}),
            })
        })

        const { result } = renderHook(() => AddStocksHelper());

        await act(async () => {
            accessToken = await result.current.getAccessToken("test_public_token")
        })

        expect(accessToken).toBe('access-sandbox-c314b575-cc3d-4897-ae93-c792eb4c2d7c')
    })

    it('test get balance', async () => {
        global.fetch =  jest.fn( async () => {
            return Promise.resolve({
              status: 200, json: () => ({"accounts": [{"balances": {"current": 100}}]}),
            })
        })

        const { result } = renderHook(() => AddStocksHelper());

        await act(async () => {
            balance = await result.current.getBalance("test_access_token")
        })

        expect(balance).toBe('83.00')
    })

    it('test get transaction', async () => {
        global.fetch =  jest.fn( async () => {
            return Promise.resolve({
              status: 200, json: () => transaction,
            })
        })

        const { result } = renderHook(() => AddStocksHelper());

        await act(async () => {
            transaction_response = await result.current.getTransaction("test_access_token")
        })

        expect(transaction_response).toBe(transaction)
    })

    it('test get logo', async () => {
        global.fetch =  jest.fn( async () => {
            return Promise.resolve({
              status: 200, json: () => ({logo: 'test_logo'}),
            })
        })

        const { result } = renderHook(() => AddStocksHelper());

        await act(async () => {
            logo = await result.current.getLogo({metadata: {institution: {name: "test_institution"}}})
        })

        expect(logo).toBe('test_logo')
    })

    it('test get stocks', async () => {
        global.fetch =  jest.fn( async () => {
            return Promise.resolve({
              status: 200, json: () => ({holdings: "test_holding", securities: "test_securities"}),
            })
        })

        const { result } = renderHook(() => AddStocksHelper());

        await act(async () => {
            data = await result.current.getStocks("test_access_token")
        })

        expect(data).toStrictEqual(["test_holding", "test_securities"])
    })

    it('test add account', async () => {
        global.fetch =  jest.fn( async () => {
            return Promise.resolve({
              status: 200, json: () => "success",
            })
        })

        const { result } = renderHook(() => AddStocksHelper());

        await act(async () => {
            await result.current.addAccount({_id: "test_id", meta: {name: "test_name"}}, {metadata: {institution: {name: "test_institution", id: "test_id"}}}, "test_access_token", 100, "test_logo")
        })
    })

    it('test add transaction', async () => {
        global.fetch =  jest.fn( async () => {
            return Promise.resolve({
              status: 200, json: () => "success",
            })
        })

        const { result } = renderHook(() => AddStocksHelper());

        await act(async () => {
            await result.current.addTransaction({account_id: "test_id", investment_transaction_id: "test_investment_transaction_id", security_id: "test_security_id", date: "test_date", name: "test_name", quantity: "test_quantity", amount: 100, price: 10, fees: 5}, {accounts: [{account_id: "test_account_id"}]})
        })
    })

    it('test add stock', async () => {
        global.fetch =  jest.fn( async () => {
            return Promise.resolve({
              status: 200, json: () => "success",
            })
        })

        const { result } = renderHook(() => AddStocksHelper());

        await act(async () => {
            await result.current.addStock({institution_price: 100, quantity: 1, account_id: "test_account_id"}, {name: "test_name", ticker_symbol: "test_ticker_symbol", security_id: "test_security_id"})
        })
    })
})