import CryptoInsights from "../../screens/cryptocurrency/CryptoInsights";
import {render, screen, act, waitFor, fireEvent} from "@testing-library/react-native";
import cryptoWalletInsights from './fixtures/cryptoWalletInsights.json'
import cryptoExchangeInsights from './fixtures/cryptoExchangeInsights.json'
import emptyCryptoWalletInsights from './fixtures/emptyCryptoWalletInsights.json'
import emptyCryptoExchangeInsights from './fixtures/emptyCryptoExchangeInsights.json'


describe('<CryptoInsights />', () => {

  const params = {
    navigation: {
      navigate: jest.fn(),
      goBack: jest.fn()
    }
  };

  beforeEach(() => {

    global.fetch =  jest.fn( async (api) => {
      const cryptoComparePattern = /cryptocompare/
      const walletPattern = /crypto_wallets/
      const exchangePattern = /crypto-exchanges/

      if (cryptoComparePattern.test(api)) {
        return Promise.resolve({
          status: 200, json: () => ({'GBP': 5})
        })
      } else if (walletPattern.test(api)) {
        return Promise.resolve({
          status: 200, json: () => cryptoWalletInsights
        })
      } else if (exchangePattern.test(api)) {
        return Promise.resolve({
          status: 200, json: () => cryptoExchangeInsights
        })
      }

    })

  })

  it('snapshot test', async () => {

    const snapshot = render(<CryptoInsights {...params} />)

    await act(async () => {
      expect(snapshot).toMatchSnapshot()
    })

  })

  it('display insights test', async () => {

    const snapshot = render(<CryptoInsights {...params} />)

    await act(async () => {

      await waitFor(() => {
        expect(screen.getByText('0.20841539 BTC')).toBeDefined()
        expect(screen.getByText('1.33461905 DASH')).toBeDefined()

        expect(screen.getByText('+241927.83346547 BTC')).toBeDefined()
        expect(screen.getByText('-241927.62541684 BTC')).toBeDefined()

        expect(screen.getByText('+886343.72139693 DASH')).toBeDefined()
        expect(screen.getByText('-886342.38677788 DASH')).toBeDefined()

        expect(screen.getByText('1393.863089464698 BTC')).toBeDefined()
        expect(screen.getByText('10.049040082741936 DASH')).toBeDefined()

        expect(screen.getByText('Binance')).toBeDefined()
        expect(screen.getByText('2021-01-29 13:31:41')).toBeDefined()

      })

    })

    expect(snapshot).toMatchSnapshot()

  })

  it('fetch insights fail test', async () => {

    global.fetch =  jest.fn( async () => {
      return Promise.resolve({
        status: 200, json: () => Promise.reject(),
      })
    })

    const snapshot = render(<CryptoInsights {...params} />)

    await act(async () => {

      expect(screen.getAllByText('There are no wallet insights to display. Try connect a crypto wallet.'))
      expect(screen.getByText('Loading...'))

      expect(snapshot).toMatchSnapshot()

    })

  })

  it('display empty insights test', async () => {

    global.fetch =  jest.fn( async (api) => {
      const cryptoComparePattern = /cryptocompare/
      const walletPattern = /crypto_wallets/
      const exchangePattern = /crypto-exchanges/

      if (cryptoComparePattern.test(api)) {
        return Promise.resolve({
          status: 200, json: () => ({'GBP': 5})
        })
      } else if (walletPattern.test(api)) {
        return Promise.resolve({
          status: 200, json: () => emptyCryptoWalletInsights
        })
      } else if (exchangePattern.test(api)) {
        return Promise.resolve({
          status: 200, json: () => emptyCryptoExchangeInsights
        })
      }

    })

    const snapshot = render(<CryptoInsights {...params} />)

    await act(async () => {

      expect(screen.getAllByText('There are no wallet insights to display. Try connect a crypto wallet.'))

      expect(snapshot).toMatchSnapshot()

    })

  })

  it('display loading insights test', async () => {

    global.fetch =  jest.fn(() => Promise.resolve())

    const snapshot = render(<CryptoInsights {...params} />)

    await act(async () => {

      expect(screen.getAllByText('Loading...'))

    })

    // Test loading of crypto exchange wallets

    global.fetch =  jest.fn( async (api) => {
      const cryptoComparePattern = /cryptocompare/
      const walletPattern = /crypto_wallets/
      const exchangePattern = /crypto-exchanges/

      if (cryptoComparePattern.test(api)) {
        return Promise.resolve({
          status: 200, json: () => ({'GBP': 5})
        })
      } else if (walletPattern.test(api)) {
        return Promise.resolve({
          status: 200, json: () => emptyCryptoWalletInsights
        })
      } else if (exchangePattern.test(api)) {
        return Promise.resolve({
          status: 200, json: () => {}
        })
      }

    })

    render(<CryptoInsights {...params} />)

    await act(async () => {

      expect(screen.getAllByText('Loading...'))

    })

  })

})