import {act, fireEvent, render, screen, waitFor} from "@testing-library/react-native";
import CryptoWalletConnector from "../../screens/crypto_wallet/CryptoWalletConnector";

describe('<CryptoWalletConnector />', () => {

  const params = {
    route: {
      params: {
          currentBid: 'whatever-id',
          connectWallet: jest.fn(async () => {return Promise}),
        },
    },
    navigation: {
      navigate: jest.fn(),
    }
  };

  it('snapshot test', async () => {
    const snapshot = render(<CryptoWalletConnector {...params} />)

    await act(async () => {
      expect(snapshot).toMatchSnapshot()

      // Test navigation
      const connectButton = screen.getAllByText('Connect Wallet')[1]
      fireEvent.press(connectButton)

    })
  })

  it('address change test', async () => {
    const testValue = "Test"

    const { getByTestId } = render(<CryptoWalletConnector {...params} />)
    const textInput = getByTestId('addressInput')
    fireEvent.changeText(textInput, testValue)

  })

})