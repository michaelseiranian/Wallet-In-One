import React, {useEffect, useState} from "react";
import {
  TouchableOpacity,
  SafeAreaView,
  ScrollView,
  StyleSheet,
  Text,
  View,
  Alert, ActivityIndicator,
} from "react-native";
import useCryptoWallet from "../crypto_wallet/useCryptoWallet";
import useCryptoExchange from "../cryptoExchanges/useCryptoExchange";
import CryptoListWalletItem from "../crypto_wallet/CryptoListWalletItem";
import useCryptoExchangeBalances from "../cryptoExchanges/useCryptoExchangeBalances";
import ExchangeAsset from "../cryptoExchanges/ExchangeAsset";
import { useTheme } from '../../src/theme/ThemeProvider'
import * as SecureStore from "expo-secure-store";
import { api_url } from '../../authentication';
import {useIsFocused} from "@react-navigation/native";

/**
 * Component that displays a list of users crypto wallet and exchanges, with navigation paths to insights, and a crypto
 * connector, along with an update button, to refresh the values of the crypto assets..
 */
export default function CryptoList(props) {
  const { wallets, listWallets, connectWallet, removeWallet } = useCryptoWallet();
  const { exchanges, fetchExchanges, removeExchange } = useCryptoExchange();
  const { balances, fetchBalances } = useCryptoExchangeBalances();
  const {dark, colors, setScheme} = useTheme();
  const isFocused = useIsFocused();
  const [loading, setLoading] = useState(false);

  const styles = StyleSheet.create({
    cryptoWalletTitle: {
      fontWeight: "900",
      fontSize: 40,
      alignSelf: "center",
      paddingVertical: 10,
    },
    cryptoWalletSubtitle: {
      fontWeight: "900",
      fontSize: 30,
      alignSelf: "center",
    },

    walletList: {
      marginHorizontal: 10,
      marginBottom: 30,
    },
    button: {
      padding: 10,
      borderRadius: 10,
      marginVertical: 4,
      marginHorizontal: 8,
      backgroundColor: colors.primary,
      alignSelf: 'center',
    },
    buttonText: {
      textAlign: 'center',
      fontWeight: 'bold',
      color: colors.text,
    },
    refreshButton: {
      position: 'absolute',
      top: 0,
      right: 10,
      backgroundColor: colors.primary,
      borderRadius: 30,
      padding: 10,
      marginTop: 10
    },
  });

  useEffect(() => {
    listWallets();
    fetchExchanges();
    fetchBalances();
  }, [isFocused]);

  /**
   * Function that handles the submission of the update button, which will call the backend to update the values of both
   * the cryptocurrency wallets and the exchanges.
   */
  const handleSubmit = async () => {

    setLoading(true)

    try {
      const response = await fetch(api_url + '/crypto_wallets/update', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Token ${await SecureStore.getItemAsync("token")}`,
        },
        body: JSON.stringify({ }),
      });
      const statusCode = response.status;
      if (statusCode === 200) {
        await listWallets();
      }
    } catch (error) {
      console.error(error);
    }

    try {
      const response = await fetch(api_url + '/crypto-exchanges/update', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Token ${await SecureStore.getItemAsync("token")}`,
        },
        body: JSON.stringify({ }),
      });
      const data = await response.json();
      const statusCode = response.status;
      if (statusCode === 200) {
        Alert.alert('Success', 'Updated account data successfully!');
      } else {
        Alert.alert('Error', data["error"]);
      }
    } catch (error) {
      console.error(error);
      Alert.alert('Error', 'An error occurred while updating account info.');
    }

    setLoading(false)
  };

  return (
    <SafeAreaView style={{ flex: 1, backgroundColor: colors.background }}>
      <ScrollView>

        <View style={{flexDirection:'row', justifyContent: 'center'}}>
          <TouchableOpacity
            style={styles.button}
            onPress={() => props.navigation.navigate("Crypto Wallet Insights")}
          >
            <Text style={styles.buttonText}>Insights</Text>
          </TouchableOpacity>

          {loading
            ?
            <TouchableOpacity
              style={styles.button}
            >
              <ActivityIndicator color={colors.text}/>
            </TouchableOpacity>
            :
            <TouchableOpacity
              style={styles.button}
              onPress={() => handleSubmit()}
            >
              <Text style={styles.buttonText}>Update</Text>
            </TouchableOpacity>
          }


        </View>
        
        <Text style={[styles.cryptoWalletSubtitle, {color: colors.text, marginTop: 10}]}>Wallets</Text>

        <View style={[styles.walletList]}>
          {
            wallets.length === 0
              ?
              <Text style={{color: colors.text}}>There are no wallets to display. Try connect a crypto wallet.</Text>
              :
              <View>
                {
                  wallets.map((item) =>
                    <CryptoListWalletItem key={item.id} id={item.id} item={item} removeWallet={removeWallet} navigation={props.navigation} />)
                }
              </View>
          }

        </View>

        <Text style={[styles.cryptoWalletSubtitle, {color: colors.text}]}>Exchanges</Text>
        <View style={[styles.walletList]}>
          {
            exchanges.length === 0
              ?
              <Text style={{color: colors.text}}>There are no exchanges to display. Try connect a crypto exchange.</Text>
              :
              <View>
                {
                  exchanges.map((item) =>
                    <ExchangeAsset key={item.id} item={item} balances={balances} removeExchange={removeExchange} navigation={props.navigation} />)
                }
              </View>
          }
          </View>
      </ScrollView>
    </SafeAreaView>
  );
}