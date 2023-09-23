import {render, act, fireEvent, screen, waitFor} from "@testing-library/react-native";
import CryptoListWalletItem from "../../screens/crypto_wallet/CryptoListWalletItem";


describe('<CryptoListWalletItem />', () => {

  const navigate = jest.fn();

  beforeEach(() => {
    global.fetch =  jest.fn( async () => {
      return Promise.resolve({
        status: 200, json: () => ({'GBP': 5}),
      })
    })
  })

  afterEach(() => {
    global.fetch.mockClear();
    delete global.fetch;
  })

  it('snapshot test', async () => {
    const snapshot = render(<CryptoListWalletItem item={{symbol: '-', id: 1}} navigation={{navigate}} />)

    await act(async () => {
      expect(snapshot).toMatchSnapshot()

      // Test navigation
      fireEvent.press(await screen.getByText('-'))

    })
  })

  it('wallet data test', async () => {
    const snapshot = render(<CryptoListWalletItem item={{symbol: 'BTC', cryptocurrency: 'Bitcoin', balance: 10.01}} />)

    await act(async () => {

      expect(screen.getByText("Bitcoin"))
      expect(screen.getByText("10.01 BTC"))

      await waitFor(() => {
        expect(screen.getByText('£50.05')).toBeDefined()
      })

      expect(snapshot).toMatchSnapshot()

    })
  })

  it('fetch fail test', async() => {

    global.fetch =  jest.fn( async () => {
      return Promise.resolve({
        status: 200, json: () => Promise.reject(),
      })
    })

    const snapshot = render(<CryptoListWalletItem item={{symbol: 'BTC', cryptocurrency: 'Bitcoin', balance: 10.01}} />)

    await act(async () => {

      expect(screen.getByText("Bitcoin"))
      expect(screen.getByText("10.01 BTC"))

      await waitFor(() => {
        expect(screen.getByText('£0.00')).toBeDefined()
      })

      expect(snapshot).toMatchSnapshot()

    })
  })

})