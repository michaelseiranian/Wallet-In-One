import { NavigationContainer,  DefaultTheme, DarkTheme} from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import TransactionData from './screens/stocks/StockTransactionData';
import LineChartScreen from "reactnative/screens/charts/LineChart.js";
import StockDetails from './screens/stocks/StockDetails';
import { useContext, useEffect } from 'react';
import { Text } from 'react-native';
import MainStackNavigator from "./screens/Main Account/MainStackNavigator";

// Screens
import StartScreen from './screens/pre_logged_in/StartScreen';
import SignUpScreen from './screens/pre_logged_in/SignUpScreen';
import LoginScreen from './screens/LoginScreen';
import HomePage from './screens/charts/HomePage';
import SettingsPage from './screens/SettingsPage';
import AboutUsScreen from './screens/pre_logged_in/AboutUsScreen';
import DeveloperInfoScreen from './screens/pre_logged_in/DeveloperInfoScreen';
import BankInsights from './screens/banking/BankInsights';

import AddBankScreen from './screens/banking/AddBankScreen'
import BankAccountsScreen from './screens/banking/BankAccountsScreen'
import BankTransactionsScreen from './screens/banking/BankTransactionsScreen'

import { initAuthState } from './authentication';
import { userContext } from './data';

import { useTheme } from 'reactnative/src/theme/ThemeProvider'

import AntDesign from 'react-native-vector-icons/AntDesign';
import MaterialCommunityIcons from 'react-native-vector-icons/MaterialCommunityIcons'

import { setStatusBarHidden } from 'expo-status-bar';
import CryptoWalletDetail from "./screens/crypto_wallet/CryptoWalletDetail";

import StockAsset from './screens/stocks/StockAsset';
import ExchangeTransactions from './screens/cryptoExchanges/ExchangeTransactions';

const Tab = createBottomTabNavigator();
const Stack = createStackNavigator();

export default function Navigation() {

    const [user, setUser] = useContext(userContext)
    const {dark, colors, setScheme} = useTheme();

    useEffect(()=>{initAuthState(user, setUser);}, []);

  return (
    <NavigationContainer
      theme={dark ? DarkTheme: DefaultTheme}
    >
      {user.signedIn ? (
        <Tab.Navigator
          initialRouteName='Home Page'
          screenOptions={
          {
            headerStyle: {backgroundColor: colors.background},
            headerTitleStyle: {color: colors.text},
            tabBarStyle: {backgroundColor: colors.background},
            tabBarShowLabel: false,
            tabBarHideOnKeyboard: true,
          }}
        >
          <Tab.Screen
            name='Home'
            component={HomePageNavigator}
            options={{
              headerShown: false,
              tabBarIcon: ({ focused }) => (
                <Text style={{ color: focused ? colors.primary : colors.text }}>
                  <AntDesign name="home" size={30} />
                </Text>
              ),
            }}
          />
          <Tab.Screen
            name="All Accounts"
            component={MainStackNavigator}
            options={{
              headerShown: false,
              tabBarIcon: ({ focused }) => (
                <Text style={{ color: focused ? colors.primary : colors.text }}>
                  <AntDesign name="user" size={30} />
                </Text>
              ),
            }}
          />
          <Tab.Screen
            name="Settings"
            component={SettingsPage}
            options={{
              tabBarIcon: ({ focused }) => (
                <Text style={{color: focused ? colors.primary : colors.text}}>
                  <AntDesign name="setting" size={30}/>
                </Text>
              ),
            }}
          />
        </Tab.Navigator>
      ) : (
        <Stack.Navigator
        screenOptions={
          {
            headerStyle: {backgroundColor: colors.background},
            headerTitleStyle: {color: colors.text},
          }
        }
        >
          <Stack.Screen
            name='Start'
            component={StartScreen}
            options={{headerShown: false}}
          />
          <Stack.Screen
            name='Sign Up'
            component={SignUpScreen}
          />
          <Stack.Screen
            name='Login'
            component={LoginScreen}
          />
          <Stack.Screen
            name='Settings'
            component={SettingsPage}
          />
          <Stack.Screen
            name='About Us'
            component={AboutUsScreen}
            options={{headerShown: false}}
          />
          <Stack.Screen
            name='Developer Info'
            component={DeveloperInfoScreen}
            options={{headerShown: false}}
          />

        </Stack.Navigator>
      )}
    </NavigationContainer>
  )
}

function HomePageNavigator() {

  const {dark, colors, setScheme} = useTheme();
  
  return (
    <Stack.Navigator
      screenOptions={
        {
          headerStyle: {backgroundColor: colors.background},
          headerTitleStyle: {color: colors.text},
        }}
    >
      <Stack.Screen
        name='Home Page'
        component={HomePage}
      />
      <Stack.Screen
        name='Bank Transactions'
        component={BankTransactionsScreen} />
      <Stack.Screen
        name='Wallet Detail'
        component={CryptoWalletDetail} />
      <Stack.Screen
        name='Stock Account Transactions'
        component={StockAsset} />
        <Stack.Screen
        name='ExchangeTransactions'
        component={ExchangeTransactions} />
      <Stack.Screen name="TransactionData" component={TransactionData} />
      <Stack.Screen name="LineGraph" component={LineChartScreen} />
      <Stack.Screen name="StockDetails" component={StockDetails} />
    </Stack.Navigator>)
}

