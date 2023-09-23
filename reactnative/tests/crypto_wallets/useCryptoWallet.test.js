import useCryptoWallet from "../../screens/crypto_wallet/useCryptoWallet";
import {renderHook, act} from "@testing-library/react-native";
import { Alert } from 'react-native';
import cryptoWallets from './fixtures/cryptoWallets.json'
import cryptoWallet from './fixtures/cryptoWallet.json'


describe('<useCryptoWallet />', () => {

  afterEach(() => {
    global.fetch.mockClear();
    delete global.fetch;
  })

  it('test list wallets', async () => {
    global.fetch =  jest.fn( async () => {
      return Promise.resolve({
        status: 200, json: () => cryptoWallets,
      })
    })

    const { result } = renderHook(() => useCryptoWallet());

    await act(async () => {
      await result.current.listWallets()
    })

    expect(result.current.wallets).toBe(cryptoWallets)

  })

  it('test list wallets fail', async () => {
    global.fetch =  jest.fn( async () => {
      return Promise.resolve({
        status: 200, json: () => Promise.reject(),
      })
    })

    const { result } = renderHook(() => useCryptoWallet());

    await act(async () => {
      await result.current.listWallets()
    })

    expect(result.current.wallets).toEqual([])

  })

  it('test connect wallet', async () => {
    global.fetch =  jest.fn( async () => {
      return Promise.resolve({
        status: 201, json: () => cryptoWallet,
      })
    })

    const { result } = renderHook(() => useCryptoWallet());

    await act(async () => {
      await result.current.connectWallet(cryptoWallet.cryptocurrency, cryptoWallet.symbol, cryptoWallet.address)
    })

    expect(result.current.wallets).toEqual([cryptoWallet])

  })

  it('test connect wallet not ok', async () => {
    global.fetch =  jest.fn( async () => {
      return Promise.resolve({
        status: 404, json: () => ({address: ['Error']}),
      })
    })

    jest.spyOn(Alert, 'alert');

    const { result } = renderHook(() => useCryptoWallet());

    await act(async () => {
      await result.current.connectWallet(cryptoWallet.cryptocurrency, cryptoWallet.symbol, cryptoWallet.address)
    })

    expect(result.current.wallets).toEqual([])
    expect(Alert.alert).toHaveBeenCalledWith("Connection Fault", "Error - error")

  })

  it('test connect wallet fail', async () => {
    global.fetch =  jest.fn( async () => {
      return Promise.reject()
    })

    const { result } = renderHook(() => useCryptoWallet());

    await act(async () => {
      await expect(async () => {
        await result.current.connectWallet(cryptoWallet.cryptocurrency, cryptoWallet.symbol, cryptoWallet.address)
      }).rejects.toThrow()
    })

  })

  it('test delete wallet', async () => {
    global.fetch =  jest.fn( async () => {
      return Promise.resolve({
        status: 201, json: () => ({id: 1, address: '0x0'})
      })
    })

    const { result } = renderHook(() => useCryptoWallet());
    await act(async () => {
      await result.current.connectWallet('Bitcoin', 'BTC', '0x0')
    })

    global.fetch =  jest.fn( async () => {
      return Promise.resolve({
        status: 204, json: () => {}
      })
    })

    await act(async () => {
      await result.current.removeWallet(1)
    })

    expect(result.current.wallets).toEqual([])

  })

  it('test delete wallet fail', async () => {
    global.fetch =  jest.fn( async () => {
      return Promise.reject()
    })

    const { result } = renderHook(() => useCryptoWallet());

    await act(async () => {
      await result.current.removeWallet(2)
    })

    expect(result.current.wallets).toEqual([])

  })

})