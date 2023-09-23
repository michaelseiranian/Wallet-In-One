import { useState } from "react";
import * as SecureStore from "expo-secure-store";
import { BACKEND_URL } from "@env"
import { api_url } from '../../authentication';


export default function useCryptoExchange() {
  const [exchanges, setExchanges] = useState([]);
  // Fetch the crypto exchange accounts
  const fetchExchanges = async () => {
    await fetch(`${api_url}/crypto-exchanges`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Token ${await SecureStore.getItemAsync("token")}`,
        },
      })
        .then((res) => res.json())
        .then((res) => setExchanges(res))
        .catch((err) => console.log(err));
  }
  // Remove exchange backend call
  const removeExchange = async (id) => {
    await fetch(`${api_url}/crypto-exchanges`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Token ${await SecureStore.getItemAsync("token")}`,
      },
      body: JSON.stringify({
        id: id
      }),
    })
      .then(() => setExchanges(exchanges.filter(exchange => exchange.id !== id)))
      .catch((err) => console.log(err));

    }

  return { exchanges, setExchanges, fetchExchanges, removeExchange };
}