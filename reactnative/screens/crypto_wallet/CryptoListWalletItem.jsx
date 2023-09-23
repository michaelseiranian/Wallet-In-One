import {
  Image,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from "react-native";
import React, {useEffect, useState} from "react";
import getCryptoIcon from "../cryptocurrency/icons/icon";
import { useTheme } from '../../src/theme/ThemeProvider'

/**
 * Component that displays a crypto wallet within the crypto wallet list, which includes a logo, the balance of the
 * crypto wallet in its currency, and the value of the crypto wallet in pounds.
 */
export default function CryptoListWalletItem(props) {

  const [cryptoValue, setCryptoValue] = useState(0);
  const {dark, colors, setScheme} = useTheme();

  const styles = StyleSheet.create({
    walletAsset: {
      padding: 10,
      marginVertical: 5,
      borderRadius: 10,
      flexDirection: "row",
    },
    walletAssetTitle: {
      fontWeight: "700",
      flex: 1,
    },
    walletAssetImage: {
      width: 30,
      height: 30,
    },
  });

  /**
   * Function that gets the conversion rate of the target cryptocurrency into pounds and stores it in the component.
   */
  const getCryptoValue = async () => {
    await fetch(`https://min-api.cryptocompare.com/data/price?fsym=${props.item.symbol}&tsyms=GBP`)
      .then((res) => res.json())
      .then((res) => res.GBP)
      .then((res) => setCryptoValue(res))
      .catch((err) => console.log(err))
  }

  useEffect(() => {
    getCryptoValue();
  }, []);

  return (
    <TouchableOpacity
      onPress={() =>
        props.navigation.navigate("Crypto Wallet Detail",
          { id: props.item.id, value: cryptoValue * props.item.balance, removeWallet: props.removeWallet })
      }
    >
      <View style={[styles.walletAsset, {backgroundColor: colors.primary}]}>
        <View
          style={{
            alignItems: "center",
            justifyContent: "center",
            paddingRight: 10,
          }}
        >
          <Image
            style={styles.walletAssetImage}
            source={getCryptoIcon(props.item.symbol)}
          />
        </View>

        <View
          style={{
            flex: 1,
            flexDirection: "row",
            justifyContent: "space-between",
          }}
        >
          <View style={{}}>
            <Text style={{ fontSize: 25, fontWeight: "700", color: colors.text }}>
              {props.item.cryptocurrency}
            </Text>
            <Text style={[styles.walletAssetTitle, {color: colors.text}]}>
              {props.item.balance} {props.item.symbol}
            </Text>

            <Text style={[styles.walletAssetTitle, {color: colors.text}]}>£{(cryptoValue * props.item.balance).toFixed(2)}</Text>
          </View>

        </View>
      </View>
    </TouchableOpacity>
  );
}