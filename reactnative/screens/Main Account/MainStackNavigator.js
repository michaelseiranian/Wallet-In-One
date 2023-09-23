import React from "react";
import {LogBox, Text, TouchableOpacity} from "react-native";
import { createStackNavigator } from "@react-navigation/stack";
import { View } from "react-native";

//Bank Screens
import AddBankScreen from "../banking/AddBankScreen";
import BankAccountsScreen from "../banking/BankAccountsScreen";
import BankTransactionsScreen from "../banking/BankTransactionsScreen";
import MainAccountPage from "./MainAccountPage";
import BankInsights from "../banking/BankInsights";

//Crypto Wallet Screens
import CryptoList from "../cryptocurrency/CryptoList";
import CryptoWalletDetail from "../crypto_wallet/CryptoWalletDetail";
import CryptoWalletConnector from "../crypto_wallet/CryptoWalletConnector";
import CryptoConnector from "../cryptocurrency/CryptoConnector"

//Crypto Exchanges Screens
import ExchangeAsset from "../cryptoExchanges/ExchangeAsset";
import ExchangeTransactions from "../cryptoExchanges/ExchangeTransactions";

import { useTheme } from 'reactnative/src/theme/ThemeProvider'
import CryptoInsights from "../cryptocurrency/CryptoInsights";

//Crypto Exchanges Screens
import ExchangeCredentials from "../cryptoExchanges/ExchangeCredentials";

import StockAsset from "../stocks/StockAsset";
import SuccessComponent from "../stocks/ListStocksScreen";
import TransactionData from "../stocks/StockTransactionData";
import LineChartScreen from "reactnative/screens/charts/LineChart.js";
import PlaidComponent from "../stocks/AddStocksScreen";
import StockDetails from "../stocks/StockDetails";
import StockInsight from "../stocks/StocksInsightScreen";

const Stack = createStackNavigator();

export default function MainStackNavigator() {

  const {dark, colors, setScheme} = useTheme();

  return (
    <Stack.Navigator
      initialRouteName="Main Account"
      screenOptions={
        {
          headerStyle: {backgroundColor: colors.background},
          headerTitleStyle: {color: colors.text},
          tabBarStyle: {backgroundColor: colors.background},
          tabBarShowLabel: false,
          tabBarHideOnKeyboard: true,
        }}
    >
      <Stack.Screen name="Accounts" component={MainAccountPage} />
      <Stack.Screen
        name="Bank Accounts"
        component={BankAccountsScreen}
        options={({ navigation }) => ({
          headerRight: () => (
            <TouchableOpacity
              style={{ marginRight: 15 }}
              onPress={() => navigation.navigate("Add Bank Account")}
            >
              <Text style={{ color: "#007AFF" }}>Add</Text>
            </TouchableOpacity>
          ),
        })}
      />
      <Stack.Screen name="Add Bank Account" component={AddBankScreen} />
      <Stack.Screen name="Bank Transactions" component={BankTransactionsScreen}/>
      <Stack.Screen name="All Bank Transactions" component={BankTransactionsScreen}/>

      <Stack.Screen name="Bank Insights" component={BankInsights} />

      <Stack.Screen 
        name="Crypto Wallets & Exchanges"
        component={CryptoList}
        options={({ navigation }) => ({
          headerRight: () => (
            <TouchableOpacity 
              style={{ marginRight: 15 }} 
              onPress={() => navigation.navigate("Add Cryptocurrency Asset")}
            >
              <Text style={{ color: '#007AFF' }}>Add</Text>
            </TouchableOpacity>
          )
      })}/>
      <Stack.Screen
        name="Add Cryptocurrency Asset"
        component={CryptoConnector} />
      <Stack.Screen
        name="Crypto Wallet Detail"
        component={CryptoWalletDetail}
      />
      <Stack.Screen name="WalletConnector" component={CryptoWalletConnector} />
      <Stack.Screen name="Crypto Wallet Insights" component={CryptoInsights} />

      <Stack.Screen name="Exchange Credentials" component={ExchangeCredentials} />

      <Stack.Screen name="ExchangeTransactions" component={ExchangeTransactions} />

      <Stack.Screen name="Stock Account List" component={SuccessComponent}
                options={({ navigation }) => ({
                  headerRight: () => (
                    <View style={{flexDirection: "row"}}>
                    <TouchableOpacity 
                      style={{ marginRight: 15 }} 
                      onPress={() => navigation.navigate('Insights')}
                    >
                      <Text style={{ color: colors.text }}>Insights</Text>
                    </TouchableOpacity>
                    <TouchableOpacity 
                      style={{ marginRight: 15 }} 
                      onPress={() => navigation.navigate('Add Stocks Account')}
                    >
                      <Text style={{ color: colors.text }}>Add</Text>
                    </TouchableOpacity>
                    </View>
                  ),
                })}
        />
        <Stack.Screen name="Insights" component={StockInsight} />
        <Stack.Screen name="StockAsset" component={StockAsset} />
        <Stack.Screen name="TransactionData" component={TransactionData} />
        <Stack.Screen name="LineGraph" component={LineChartScreen} />
        <Stack.Screen name="Add Stocks Account" component={PlaidComponent} />
        <Stack.Screen name="StockDetails" component={StockDetails} />


    </Stack.Navigator>
  );
}

// This warning can be safely ignored.
// https://reactnavigation.org/docs/troubleshooting/#i-get-the-warning-non-serializable-values-were-found-in-the-navigation-state
LogBox.ignoreLogs([
  "Non-serializable values were found in the navigation state",
])
