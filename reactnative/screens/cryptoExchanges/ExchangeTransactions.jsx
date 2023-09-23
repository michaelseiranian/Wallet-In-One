import {Dimensions, Image, Pressable, StyleSheet, Text, View, ScrollView} from "react-native";
import * as SecureStore from 'expo-secure-store';
import React, {useEffect, useState, useCallback} from "react";
import getCryptoIcon from "../cryptocurrency/icons/icon";
import { useTheme } from '../../src/theme/ThemeProvider'
import { styles } from '../All_Styles.style.js';
import { api_url } from '../../authentication';
import {Table, Row, Cell} from 'react-native-table-component';
import BarChart from "../charts/chartComponents/barChart";
import ConditionalModal from "../Modal";
import PieChart from "../charts/chartComponents/pieChart";
import SwitchSelector from "react-native-switch-selector";

export default function ExchangeTransactions(props) {
  const [modalVisible, setModalVisible] = useState(false);
  const {dark, colors } = useTheme();
  const [exchangeTransactions, setExchangeTransactions] = useState([]);
  const [exchangeTokens, setExchangeTokens] = useState([]);
  const [balance, setBalance] = useState();
  const { item, removeExchange } = props.route.params;
  const exchange = item.id;
  const { width } = Dimensions.get("window");
  const stylesInternal = StyleSheet.create({
    container: {
      flex: 1,
      justifyContent: 'center',
      alignItems: 'center',
    },
    exchangeAsset: {
      borderRadius: 10,
      paddingTop: 20,
      paddingBottom: 20
    },
    exchangeAssetImage: {
      width: 80,
      height: 80,
    },
    largeBoldText: {
      fontWeight:"800",
      fontSize:31,
      paddingTop: 10,
      color: colors.text,
    },
    mediumBoldText: {
      fontWeight:"800",
      fontSize:25,
      paddingTop: 10, 
      color: colors.text,
      alignItems: 'center',
    },
    mediumText: {
      fontWeight:"200",
      fontSize: 19,
      paddingTop: 0,
      color: colors.text,
    },
    row: {
      flexDirection: 'row',
      alignItems: 'center',
    },
    header: {
      flexDirection: 'row',
      height: 30,
      fontWeight: "850",
      fontSize: 25,
    },
    head: {
      height: 44,
      backgroundColor: '#42b983'
    },
    table: {
      flex: 1,
      justifyContent: 'center',
      backgroundColor: colors.background,
    },

  });  

  // Fetch the transactions from backend
  let getExchangeTransactions = useCallback(async (exchange) => {
    try {
      const response = await fetch(api_url + `/crypto-exchanges/get_transactions/${exchange}/`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Token ${await SecureStore.getItemAsync("token")}`,
        },
      });
      let data = await response.json();
      setExchangeTransactions(data);
    } catch (error) {
      console.error(error);
    }
  }, []);

  // Fetch the exchange tokens
  let getExchangeTokens = useCallback(async (exchange) => {
    try {
      const response = await fetch(api_url + `/crypto-exchanges/get_token_breakdown/${exchange}/`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Token ${await SecureStore.getItemAsync("token")}`,
        },
      });
      let data = await response.json();
      setExchangeTokens(data.token_data);
      setBalance(data.balance);
    } catch (error) {
      console.error(error);
    }
  }, []);

  useEffect(() => {
    if (exchange) {
      getExchangeTransactions(exchange);
      getExchangeTokens(exchange);
    }
  }, [exchange, getExchangeTransactions, getExchangeTokens]);

  // Set the table data
  const data = exchangeTransactions.length === 1 && exchangeTransactions[0] === "empty"
  ? ["empty"]
  : {
    tableHead: ['Pair', 'Amount', 'Type', 'Date'],
    tableData: exchangeTransactions.map(transaction => [
      transaction.asset,
      transaction.amount,
      transaction.transaction_type,
      new Date(transaction.timestamp).toLocaleString("en-JP", {
        year: "numeric",
        month: "long",
        day: "numeric",
        hour: "numeric",
        minute: "numeric",
      })
    ])
  };
  // Stores switch value between pie chart and transactions
  const [chartType, setChartType] = useState("pie");
  const handleChartTypeChange = (type) => {
    setChartType(type);
  };
  const tokenList = exchangeTokens.map((val) => val.x);
  const colours = [];
  // This loop generates a unique colour for each coin for the pie chart
  for (let i = 0; i < tokenList.length; i++) {
    const token = tokenList[i];
    let hex = '';
    if (token.length >= 3) {
      for (let j = 0; j < 3; j++) {
        const charCode = token.charCodeAt(j);
        const hexByte = (charCode * 3.2).toString(16).slice(0, 2);
        hex += hexByte;
      }
      colours.push('#' + hex);
    } else {
      // less than 3 chars
      const charCode = token.charCodeAt(0);
      const hexByte = (charCode * 412).toString(16).slice(0, 6);
      colours.push('#' + hexByte);
    }
  }
  const handlePressIn = ()=>{};


  return (
    <ScrollView style={{flex: 1, backgroundColor: colors.background, paddingHorizontal: 30}}>

      {/* Back arrow and remove button */}
      <View style={[styles(dark, colors).container, {flexDirection: 'row', alignItems: "flex-end"}]}>
        {/*Remove crypto exchange button*/}
        <Pressable
          onPress={() => setModalVisible(true)}
          style={{alignItems: "center", justifyContent: "center", marginLeft: 'auto'}}>
          <View style={styles(dark, colors).smallButton}>
            <Text style={{color: colors.text, fontWeight: "800"}}>Remove</Text>
          </View>
        </Pressable>
      </View>
      {/*Confirmation for removing exchange*/}
      <View testID={'conditional-modal'}>
      <ConditionalModal
        headerText={"Remove Your Exchange"}
        bodyText={"Are you sure you want to remove your crypto exchange?"}
        visible={modalVisible}
        onEvent={() => removeExchange(item.id).then(() => props.navigation.goBack())}
        onClose={() => setModalVisible(false)}
      />
      </View>

      {/* Exchange logo, title and balance */}
      <View style={[stylesInternal.exchangeAsset, styles(dark, colors).container, {flexDirection: 'row'}]}>
        <Image testID='exchange-image'
          style={stylesInternal.exchangeAssetImage}
          source={getCryptoIcon(item.crypto_exchange_name)}/>
        <View style={{marginLeft: 10}}>
          <Text style={stylesInternal.largeBoldText}>{item.crypto_exchange_name} Exchange</Text>
          <Text style={stylesInternal.mediumText}>
            Balance: {balance === null || balance === undefined ? "Loading..." : `£${balance.toFixed(2)}`}
          </Text>
        </View>
      </View>
      {/*Switch selector to choose between pie chart and transactions table*/}
      <View style={{paddingHorizontal: 40}}>
        <SwitchSelector
          initial={0}
          onPress={value => handleChartTypeChange(value)}
          selectedColor="#fff"
          buttonColor="#7a44cf"
          borderColor="#7a44cf"
          hasPadding
          options={[    
            { label: "Coin Breakdown", value: "pie"},  
            { label: "Transactions", value: "transactions"} 
          ]}
          textStyle={{ fontWeight: 'bold', fontSize: 15 }}
          buttonMargin={1}
          height={45}
          testID='switchSelector'
        />
      </View>

      {/* Pie chart and transactions table */}    
      {chartType === "pie" ?
        <View style={stylesInternal.container}>
          <Text style={stylesInternal.mediumBoldText}>Coin Breakdown</Text>
          {exchangeTokens.length === 0 ? (
            <Text style={styles(dark, colors).text}>Loading...</Text>
          ) : exchangeTokens.length === 1 && exchangeTokens[0].x === "empty" ? (
            <Text style={styles(dark, colors).text}>No coins in this account</Text>
          ) : (
          <>  
          <View style={{ width, justifyContent: "center", alignItems: "center" }}>
          <PieChart colours={colours} data={exchangeTokens} handlePressIn={handlePressIn} labelCount={2} assetSize={27} numSize={37}/>
          </View>
          {BarChart(colours, tokenList, exchangeTokens, (tokenList.length*60), handlePressIn, colors)}
          </>
          )}
        </View>  
       : <>
      <View style={stylesInternal.container}>
        <Text style={{fontWeight:"800", fontSize:25, paddingTop: 10, color: colors.text}} testID={'transactionTitle'}>Transactions</Text>
      </View>
      {!data || data.length === 0 ? (
        <Text style={[styles(dark, colors).text, {textAlign: 'center', alignSelf: 'center'}]}>Loading...</Text>
      ) : (
        data[0] === "empty" ? (
          <Text style={[styles(dark, colors).text, {textAlign: 'center', alignSelf: 'center'}]}>
            No transaction history in this account
          </Text>
        ) : (
          <View style={[stylesInternal.table, {paddingVertical: 20}]}>
            <Table borderStyle={{ borderWidth: 2, borderColor: colors.text}}>
              <Row 
                data={data.tableHead} 
                style={{ ...stylesInternal.header, backgroundColor: dark ? "#21201E" : "#D3D3D3"}}
                textStyle={{ fontWeight: 'bold', color: colors.text, fontSize: 17 }}
              />
              {data.tableData.map((rowData, rowIndex) => (
                <Row key={rowIndex} data={rowData.map((cellData, cellIndex) => (<Cell key={cellIndex} data={cellData} textStyle={{color: colors.text}} />))} 
                  style={{ ...stylesInternal.row, backgroundColor: rowData[2] === "sell" ? dark ? "#8b0000" : "#f87171" : rowData[2] === "buy" ? dark ? "#006400" : "#90ee90" : dark ? "#323232" : "#f3f3f3"}}
                />
              ))}
            </Table>
          </View>
        )
      )}
      </>
    }
    </ScrollView>
  );

}