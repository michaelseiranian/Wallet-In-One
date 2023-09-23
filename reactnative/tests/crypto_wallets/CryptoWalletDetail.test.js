import {render, act, fireEvent, screen, waitFor} from "@testing-library/react-native";
import CryptoWalletDetail from "../../screens/crypto_wallet/CryptoWalletDetail";
import cryptoWallet from './fixtures/cryptoWallet.json'

jest.mock('react-native-wagmi-charts')


describe('<CryptoWalletDetail />', () => {

  const params = {
    route: {
      params: {
        id: 1,
        value: 50.05,
        removeWallet: jest.fn(async () => {return Promise}),
      },
    },
    navigation: {
      navigate: jest.fn(),
      goBack: jest.fn()
    }
  };

  beforeEach(() => {
    global.fetch =  jest.fn( async () => {
      return Promise.resolve({
        status: 200, json: () => cryptoWallet,
      })
    })
  })

  afterEach(() => {
    global.fetch.mockClear();
    delete global.fetch;
  })

  it('snapshot test', async () => {
    const snapshot = render(<CryptoWalletDetail {...params} />)

    await act(async () => {
      expect(snapshot).toMatchSnapshot()

      await waitFor(() => {
        expect(screen.getByText('1P5ZEDWTKTFGxQjZphgWPQUpe554WKDfHQ')).toBeDefined()
      })

      // Test button
      fireEvent.press(await screen.getByText('Transactions'))
      fireEvent.press(await screen.getByText('Breakdown'))

      await waitFor(() => {
        expect(screen.getByText('Candlestick Chart')).toBeDefined()
        fireEvent.press(screen.getByText('Candlestick Chart'))
        expect(screen.getByText('Line Chart')).toBeDefined()
        fireEvent.press(screen.getByText('Line Chart'))
      })

      fireEvent.press(await screen.getByText('Remove'))

    })

    expect(snapshot).toMatchSnapshot()

  })

  it('fetch fail test', async() => {

    global.fetch =  jest.fn( async () => {
      return Promise.resolve({
        status: 200, json: () => Promise.reject(),
      })
    })

    const snapshot = render(<CryptoWalletDetail {...params} />)

    await act(async () => {

      expect(screen.getByText('Not enough data to display graph.'))
      fireEvent.press(await screen.getByText('Transactions'))
      expect(screen.getByText('There are no transactions to display.'))

      expect(snapshot).toMatchSnapshot()

    })
  })

  it('wallet data test', async () => {
    const snapshot = render(<CryptoWalletDetail {...params} />)

    await act(async () => {

      expect(screen.getByText('£50.05'))

      await waitFor(async () => {
        expect(screen.getByText('1P5ZEDWTKTFGxQjZphgWPQUpe554WKDfHQ')).toBeDefined()
        expect(screen.getByText('0.01344898 BTC')).toBeDefined()
        expect(screen.getByText('241914.76880743 BTC')).toBeDefined()
        expect(screen.getByText('241914.75535845 BTC')).toBeDefined()
        expect(screen.getByText('847')).toBeDefined()
        expect(screen.getByText('267')).toBeDefined()
      })

    })

  })

  it('wallet transaction data test', async () => {
    const snapshot = render(<CryptoWalletDetail {...params} />)

    await act(async () => {

      fireEvent.press(await screen.getByText('Transactions'))

      await waitFor(async () => {
        expect(screen.getByText('0.0001 BTC')).toBeDefined()
        expect(screen.getByText('0.00064342 BTC')).toBeDefined()
        expect(screen.getByText('0.00000547 BTC')).toBeDefined()

      })

    })
    
  })

  it('remove wallet test', async () => {
    const snapshot = render(<CryptoWalletDetail {...params} />)

    await act(async () => {

      fireEvent.press(await screen.getByText('Remove'))
      fireEvent.press(await screen.getByText('Yes'))

    })

  })

  it('remove wallet cancel test', async () => {
    const snapshot = render(<CryptoWalletDetail {...params} />)

    await act(async () => {

      fireEvent.press(await screen.getByText('Remove'))
      fireEvent.press(await screen.getByText('No'))

    })

  })

})

