import { ConvertTransactionsToGraphCompatibleData } from "../screens/helper";
import {renderHook, act} from "@testing-library/react-native";
import transactions from "./stocks/fixtures/transactions.json"

describe('<GraphHelper />', () => {
    it('test conversion success', async () => {
        await act(async () => {
            accessToken = ConvertTransactionsToGraphCompatibleData(transactions.transactions, 100)
        })
    })
})