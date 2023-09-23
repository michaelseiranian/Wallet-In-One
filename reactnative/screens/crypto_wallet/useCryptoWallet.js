import { useState } from "react";
import * as SecureStore from "expo-secure-store";
import { BACKEND_URL } from "@env"
import {Alert} from "react-native";

/**
 * Custom react hook that connects to the backend for wallets to be retrieved, added or removed.
 */
export default function useCryptoWallet() {
  const [wallets, setWallets] = useState([]);

  /**
   * Function that retrieves a list of wallets of the requesting used from the backend.
   */
  const listWallets = async () => {
    await fetch(`${BACKEND_URL}/crypto_wallets/`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Token ${await SecureStore.getItemAsync("token")}`,
      },
    })
      .then((res) => res.json())
      .then((res) => setWallets(res))
      .catch((err) => console.log(err));
  };

  /**
   * Function that allows a wallet to be added onto the backend using the cryptocurrency, symbol and address.
   */
  const connectWallet = async (cryptocurrency, symbol, address) => {
    const response = await fetch(`${BACKEND_URL}/crypto_wallets/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Token ${await SecureStore.getItemAsync("token")}`,
      },
      body: JSON.stringify({
        cryptocurrency: cryptocurrency,
        symbol: symbol,
        address: address,
      }),
    })
      .catch((err) => console.log(err));

    const data = await response.json()

    if (response.status === 201) setWallets([...wallets, data])
    else Alert.alert("Connection Fault",
      `Error - ${data.address?.[0].toLowerCase() || data.non_field_errors}`)
  };

  /**
   * Function that removes a wallet from the backend using the id of the crypto wallet.
   */
  const removeWallet = async (id) => {
    await fetch(`${BACKEND_URL}/crypto_wallets/${id}/`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Token ${await SecureStore.getItemAsync("token")}`,
      }
    })
      .then(() => setWallets(wallets.filter(wallet => wallet.id !== id)))
      .catch((err) => console.log(err));

    }

  return { wallets, listWallets, connectWallet, removeWallet };
}
