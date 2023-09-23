import CryptoList from "../../screens/cryptocurrency/CryptoList";
import {render, screen, act, waitFor, fireEvent} from "@testing-library/react-native";
import cryptoWallets from "../crypto_wallets/fixtures/cryptoWallets.json"

describe('<CryptoList />', () => {

  const params = {
    navigation: {
      navigate: jest.fn(),
      goBack: jest.fn()
    }
  };

  beforeEach(() => {
    global.fetch =  jest.fn( async () => {
      return Promise.resolve({
        status: 200,
      })
    })
  })

  afterEach(() => {
    global.fetch.mockClear();
    delete global.fetch;
  })

  it('snapshot test', async () => {
    const snapshot = render(<CryptoList {...params} />)

    // Test navigation
    await act(async () => {
      fireEvent.press(await screen.getByText('Insights'))
    })

    expect(snapshot).toMatchSnapshot()

  })

  it('display wallets and exchanges test', async () => {

    global.fetch =  jest.fn( async (api) => {
      const exchangeBalancesPattern = /get_exchange_balances/
      const walletPattern = /crypto_wallets/
      const exchangePattern = /crypto-exchanges/

      if (exchangeBalancesPattern.test(api)) {
        return Promise.resolve({
          status: 200, json: () => ([
            {
              "x": "Binance",
              "y": 0.13,
              "id": 2
            }
          ])
        })
      } else if (walletPattern.test(api)) {
        return Promise.resolve({
          status: 200, json: () => cryptoWallets
        })
      } else if (exchangePattern.test(api)) {
        return Promise.resolve({
          status: 200, json: () => cryptoWallets
        })
      }

    })
    const snapshot = render(<CryptoList {...params} />)

    await act(async () => {

    })

  })

  it('display empty wallets and empty exchanges test', async () => {
    const snapshot = render(<CryptoList {...params} />)

    await act(async () => {
      expect(screen.getByText("There are no wallets to display. Try connect a crypto wallet."))
      expect(screen.getByText("There are no exchanges to display. Try connect a crypto exchange."))
    })

  })

  it('update crypto wallet and exchange test', async () => {
    global.fetch =  jest.fn( async (api) => {
      const exchangeBalancesPattern = /get_exchange_balances/
      const walletPattern = /crypto_wallets/
      const exchangePattern = /crypto-exchanges/

      if (exchangeBalancesPattern.test(api)) {
        return Promise.resolve({
          status: 200, json: () => ([
            {
              "x": "Binance",
              "y": 0.13,
              "id": 2
            }
          ])
        })
      } else if (walletPattern.test(api)) {
        return Promise.resolve({
          status: 200, json: () => cryptoWallets
        })
      } else if (exchangePattern.test(api)) {
        return Promise.resolve({
          status: 200, json: () => cryptoWallets
        })
      }

    })

    const snapshot = render(<CryptoList {...params} />)

    await act(async () => {
      fireEvent.press(await screen.getByText('Update'))
    })

    expect(snapshot).toMatchSnapshot()

  })

  it('update invalid crypto wallet and exchange test', async () => {
    global.fetch =  jest.fn( async (api) => {
      const exchangeBalancesPattern = /get_exchange_balances/
      const walletPattern = /crypto_wallets/
      const exchangePattern = /crypto-exchanges/

      if (exchangeBalancesPattern.test(api)) {
        return Promise.resolve({
          status: 200, json: () => ([
            {
              "x": "Binance",
              "y": 0.13,
              "id": 2
            }
          ])
        })
      } else if (walletPattern.test(api)) {
        return Promise.resolve({
          status: 400, json: () => cryptoWallets
        })
      } else if (exchangePattern.test(api)) {
        return Promise.resolve({
          status: 400, json: () => cryptoWallets
        })
      }

    })

    const snapshot = render(<CryptoList {...params} />)

    await act(async () => {
      fireEvent.press(await screen.getByText('Update'))
    })

    expect(snapshot).toMatchSnapshot()

  })

  it('update invalid crypto wallet and exchange test', async () => {
    global.fetch =  jest.fn( async (api) => {
      const exchangeBalancesPattern = /get_exchange_balances/
      const walletPattern = /crypto_wallets/
      const exchangePattern = /crypto-exchanges/

      if (exchangeBalancesPattern.test(api)) {
        return Promise.resolve({
          status: 200, json: () => ([
            {
              "x": "Binance",
              "y": 0.13,
              "id": 2
            }
          ])
        })
      } else if (walletPattern.test(api)) {
        return Promise.reject()
      } else if (exchangePattern.test(api)) {
        return Promise.resolve({
          status: 400, json: () => Promise.reject()
        })
      }

    })

    const snapshot = render(<CryptoList {...params} />)

    await act(async () => {
      fireEvent.press(await screen.getByText('Update'))
    })

  })

})