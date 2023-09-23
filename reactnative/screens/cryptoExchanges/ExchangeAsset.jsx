import {
    Image,
    Pressable,
    StyleSheet,
    Text,
    TouchableOpacity,
    TouchableWithoutFeedback,
    View,
  } from "react-native";
import React, {useEffect, useState, useCallback} from "react";
import getCryptoIcon from "../cryptocurrency/icons/icon";
import { useTheme } from 'reactnative/src/theme/ThemeProvider';
import { api_url } from "../../authentication";
import * as SecureStore from 'expo-secure-store';

export default function ExchangeAsset(props) {
  // Dark mode variables
  const {dark, colors, setScheme} = useTheme();

  const styles = StyleSheet.create({
    exchangeAsset: {
      padding: 10,
      marginVertical: 5,
      borderRadius: 10,
      flexDirection: "row",
    },
    exchangeAssetTitle: {
      fontWeight: "700",
      flex: 1,
    },
    exchangeAssetImage: {
      width: 30,
      height: 30,
    },
  });
    
  
    // Render script
    return (
        // Navigate to ExchangeTransactions on press
      <TouchableWithoutFeedback
        onPress={() =>
          props.navigation.navigate("ExchangeTransactions",
            { item: props.item, removeExchange: props.removeExchange})
        }
        testID="exchangeAsset"
      >
        <View style={[styles.exchangeAsset, {backgroundColor: colors.primary}]}>
          <View
            style={{
              alignItems: "center",
              justifyContent: "center",
              paddingRight: 10,
            }}
          >
              {/*Load crypto exchange logo*/}
            <Image
              style={styles.exchangeAssetImage}
              source={getCryptoIcon(props.item.crypto_exchange_name)}
            />
          </View>
  
          <View
            style={{
              flex: 1,
              flexDirection: "row",
              justifyContent: "space-between",
            }}
          >
              {/*Write the name on the asset card*/}
            <View style={{}}>
              <Text style={{ fontSize: 25, fontWeight: "700", color: colors.text }}>
                {props.item.crypto_exchange_name}
              </Text>
                {/*Show loading on Total balance if empty, else show the actual balance*/}
              {props.balances.length == 0 ? (
                <Text style={[styles.exchangeAssetTitle, {color: colors.text}]}>Total Balance: £Loading...</Text>
              ) : (
                <Text style={[styles.exchangeAssetTitle, {color: colors.text}]}>
                  Total Balance: £{props.balances.find(balance => balance.id === props.item.id)?.y.toFixed(2) || '0.00'}
                </Text>
              )}
            </View>
  
          </View>
        </View>
      </TouchableWithoutFeedback>
    );
  }