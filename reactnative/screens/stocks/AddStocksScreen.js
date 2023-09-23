import React, { useState, useEffect,useRef  } from 'react';
import { Image } from 'react-native';
import PlaidLink from '@burstware/expo-plaid-link'
import { useIsFocused } from '@react-navigation/native';
import { auth_post } from '../../authentication';
import { useTheme } from "reactnative/src/theme/ThemeProvider";
import AddStocksHelper from './AddStocksHelper';
import { styles } from "reactnative/screens/All_Styles.style.js";
import ConditionalModal from '../Modal';

import { StyleSheet, Pressable, View, Animated} from 'react-native';

/**
 * Component that displays the Plaid SDK for connecting Stock Accounts to the app
 */

const PlaidComponent = ({ navigation }) => {
  const [linkToken, setLinkToken] = useState('');
  const isFocused = useIsFocused();
  const {getAccessToken, getBalance, getTransaction, addAccount, addTransaction, addStock, getLogo, getStocks} = AddStocksHelper();
  let access_token = ''
  let balance = ''
  let image = ''
  let fetched_transaction_list = null
  let stocks = null
  let securities = null

  let data_response = null

  const stylesInternal = StyleSheet.create({
    modalView: {
      margin: 20,
      backgroundColor: 'white',
      borderRadius: 20,
      padding: 35,
      alignItems: 'center',
      shadowColor: '#000',
      shadowOffset: {
        width: 0,
        height: 2,
      },
      shadowOpacity: 0.25,
      shadowRadius: 4,
      elevation: 5,
    },
    button: {
      borderRadius: 20,
      padding: 10,
      elevation: 2,
    },
    buttonClose: {
      backgroundColor: '#2196F3',
    },
    textStyle: {
      color: 'white',
      fontWeight: 'bold',
      textAlign: 'center',
    },
    modalText: {
      marginBottom: 15,
      textAlign: 'center',
    },
  });

  /**
   * Whenever the screen is in focus, a call to the backend is made to access a temporary link token to open the SDK.
   */
  useEffect(() => {
  const initiatePlaidLink = async () => {
      const response = await auth_post('/stocks/initiate_plaid_link/')
      if(response.status == 200){
        setLinkToken(response.body.link_token)
      }
  };
  if(useIsFocused){initiatePlaidLink()}
}, [isFocused])


  const [modalVisible, setModalVisible] = useState(false);
  const [modalText, setModalText] = useState("Empty Modal");
  const scaleValue = useRef(new Animated.ValueXY({x: 0.5, y: 0.5})).current;

  const {dark, colors, setScheme } = useTheme();

  return (
    <>

      {
        linkToken !== undefined
          ?
          <PlaidLink
            linkToken={linkToken}
            onSuccess={async (success) => {
              let account_list = success.metadata.accounts
              access_token = await getAccessToken(success.publicToken)
              balance = await getBalance(access_token)
              let stock_response = await getStocks(access_token)
              stocks = stock_response[0]
              securities = stock_response[1]

              account_list.forEach(async element => {
                image = await getLogo(success)
                data_response = await addAccount(element, success, access_token, balance, image)

                if(data_response != 400){
                  fetched_transaction_list = await getTransaction(access_token)
                  fetched_transaction_list.investment_transactions.forEach(element => {addTransaction(element, fetched_transaction_list)})

                  stocks.forEach(element => {
                    let stockInfo = securities[stocks.indexOf(element)]
                    addStock(element, stockInfo)
                  })
                  setModalText("Stock account has been successfully added.")
                  setModalVisible(true);
                }else{
                  setModalText("Stock account has already been added!")
                  setModalVisible(true);
                }
              });
            }}
          />
          :
          <View />
      }



  <View>


  <ConditionalModal
    headerText={modalText}
    bodyText={
      <View style={stylesInternal.modalView}>
        {modalText == "Stock account has been successfully added." &&
          <Image
            style={{ width: 100, height: 100 }}
            source={{ uri: `https://cdn-icons-png.flaticon.com/512/4436/4436481.png` }}
          />
        }
        {modalText == "Stock account has already been added!" &&
          <View>
            <Image
              style={{ width: 100, height: 100 }}
              source={{ uri: `http://www.setra.com/hubfs/Sajni/crc_error.jpg` }}
            />
          </View>
        }
      </View>
    }

    visible={modalVisible}
    onClose={() =>navigation.navigate("Stock Account List")}
    cancelButtonName={"View Stock Accounts"}
    oneButton={true}
  />
  </View>
    </>
  );
};

export default PlaidComponent;