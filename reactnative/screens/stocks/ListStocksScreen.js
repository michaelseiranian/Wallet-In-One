import React, {useState, useEffect, useCallback} from 'react';
import {
  Text,
  View,
  ToastAndroid,
  Platform,
  Alert,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  Dimensions
} from 'react-native';
import * as SecureStore from 'expo-secure-store';
import { useIsFocused } from '@react-navigation/native';
import { FlatList } from 'react-native-gesture-handler';
import { api_url } from '../../authentication';
import { Button, Image } from 'react-native';
import { auth_get } from '../../authentication';
import { useTheme } from "reactnative/src/theme/ThemeProvider";
import { styles } from "reactnative/screens/All_Styles.style.js";
import Loading from '../banking/Loading';
import { ConvertTransactionsToGraphCompatibleData } from '../helper';


import LineChartScreen from '../charts/LineChart';

// Define a component that takes in a route and other props to display list of user accounts.

const SuccessComponent = ({ route, ...props }) => {
    const [list, setList] = useState()
    const isFocused = useIsFocused()
    const [transactions, setTransactions] = useState({});
    const {dark, colors, setScheme } = useTheme();
    const [loading, setLoading] = useState(true)

    const {width: SIZE} = Dimensions.get('window');

    const stylesInternal = StyleSheet.create({
      item:{
        padding: 20,
        borderRadius: 10,
        backgroundColor: colors.stock_account,
        text: colors.text,
      },
      row:{
        flexDirection: 'row',
        alignItems: 'flex-start',
      },
      name:{
        color: colors.text,
        fontWeight: 'bold',
        fontSize: 16,
        fontFamily: 'sans-serif',
      },
      ins_name:{
        color: colors.text,
        fontSize: 15,
        fontFamily: 'sans-serif',
      },
      separator: {
        height: 1,
        backgroundColor: "#3f3f46",
      },
    });

      // Use useEffect hook to fetch the list of accounts and transactions
      useEffect(() => {
        const listAccounts = async () => {
          const response = await auth_get('/stocks/list_accounts/')
          const accountList = response.body;
          if(accountList){
            // For each account, get the corresponding transactions
          accountList.forEach((account) => {
            getTransactions(account.account_id);
          });
          }
          setLoading(false)
          setList(accountList);
        }
        // Call the listAccounts function only when the screen is focused
        if (useIsFocused) {
          listAccounts();
        }        
      }, [isFocused])

      // Define a function to get transactions for a given account ID
      const getTransactions = useCallback(async (accountID) => {
        try {
          const response = await auth_get(`/stocks/list_transactions/${accountID}/`)
          const data = response.body;
          setTransactions(prevTransactions => ({
            ...prevTransactions,
            [accountID]: data
          }));
        } catch (error) {
          console.error(error);
        }
      }, []);

    // If the data is still loading, display a loading screen
    if(loading){
      return(<Loading/>)
    }
    else{
      // Otherwise, render the list of accounts
    return (
        <View style={{ ...styles(dark, colors),paddingTop:8, paddingBottom: 8 }}>
          <View>
            <FlatList 
              data={list} 
              ItemSeparatorComponent={() => <View style={{height: 8}} />} 
              style={{paddingHorizontal:8}}
              renderItem={({item, index}) =>{
              return (
                <TouchableOpacity style={{ ...stylesInternal.item }}
                  onPress={()=> {
                      props.navigation.navigate('StockAsset', {
                      accountID: item.account_id, 
                      accessToken: item.access_token, 
                      transactions: transactions[item.account_id],
                      logo: item.institution_logo,
                      balance: item.balance,
                      name: item.institution_name,
                      account_name: item.name,
                      balance_currency: item.balance_currency
                    
                  })} }>

                  <View style={stylesInternal.row}>
                    {item.institution_logo !== null && 
                      <Image
                        style={{ width: 40, height: 40 }}
                        source={{ uri: `data:image/png;base64,${item.institution_logo}` }}
                      />
                    }

                    {item.institution_logo === null && 
                      <Image
                        style={{ width: 40, height: 40 }}
                        source={{ uri: 'https://kriptomat.io/wp-content/uploads/t_hub/usdc-x2.png' }}
                      />
                    }
                    <View style={{flexDirection: "column", flex: 1}}>
                      <Text style={stylesInternal.name}>  {item.name}</Text>
                      <Text style={[stylesInternal.ins_name, {fontSize: 11}]}>   {item.institution_name} • {item.balance_currency}</Text>
                    </View>
                    <View style={{flexDirection: 'row', alignItems: 'center'}}>
                      <Text style={[stylesInternal.ins_name, {fontWeight: 'bold', fontSize: 14, height: 19}]}>£{parseInt(item.balance)}</Text>
                      <View style={{height: 16}}>
                        <Text style={[stylesInternal.ins_name, { fontSize: 12}]}>.{(item.balance).toString().split('.')[1]}</Text>
                      </View>
                    </View>

                  </View>

                  {transactions[item.account_id] && 
                    <LineChartScreen 
                      current_balance={item.balance}
                      graph_version={2}
                      height={75}
                      width={SIZE*0.85}
                      data={ConvertTransactionsToGraphCompatibleData(transactions[item.account_id], item.balance)}
                  />}

                </TouchableOpacity>
              )
            }}
            ListEmptyComponent={<Text style={styles(dark, colors).text}>{'\nYou have no stock accounts\n'}</Text>}
            />
          </View>
        </View>
      );
    }
    };

export default SuccessComponent;