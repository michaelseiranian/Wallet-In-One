import { useState } from "react";
import * as SecureStore from "expo-secure-store";
import { BACKEND_URL } from "@env"
import { api_url } from '../../authentication';

export default function useCryptoExchangeBalances() {
    const [balances, setBalances] = useState([]);
    // Fetch balances
    const fetchBalances = async () => {
      await fetch(`${api_url}/crypto-exchanges/get_exchange_balances/`, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${await SecureStore.getItemAsync("token")}`,
          },
        })
          .then((res) => res.json())
          .then((res) => setBalances(res))
          .catch((err) => console.log(err));
    }
  
    return { balances, setBalances, fetchBalances};
}