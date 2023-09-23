import {act, fireEvent, render, screen, waitFor} from "@testing-library/react-native";
import CryptoConnector from "../../screens/cryptocurrency/CryptoConnector";

describe('<CryptoConnector />', () => {

  const params = {
    navigation: {
      navigate: jest.fn(),
      goBack: jest.fn()
    }
  };


  it('snapshot test', async () => {
    const snapshot = render(<CryptoConnector {...params} />)

    expect(snapshot).toMatchSnapshot()

    // Test buttton
    fireEvent.press(await screen.getByText('Bitcoin'))
    fireEvent.press(await screen.getByText('Binance'))

  })

  it('wallet and exchange list test', async () => {
    const snapshot = render(<CryptoConnector {...params} />)

    // Wallets
    expect(screen.getByText('Bitcoin'))
    expect(screen.getByText('Bitcoin-Cash'))
    expect(screen.getByText('Litecoin'))
    expect(screen.getByText('Dogecoin'))
    expect(screen.getByText('Dash'))
    expect(screen.getByText('Groestlcoin'))
    expect(screen.getByText('Zcash'))
    expect(screen.getByText('eCash'))

    // Exchanges
    expect(screen.getByText('Binance'))
    expect(screen.getByText('GateIo'))
    expect(screen.getByText('CoinList'))
    expect(screen.getByText('CoinBase'))
    expect(screen.getByText('Kraken'))

  })

})