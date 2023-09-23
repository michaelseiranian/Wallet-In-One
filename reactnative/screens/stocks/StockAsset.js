import { View, Text, TouchableOpacity,StyleSheet,SectionList,Image,Pressable } from 'react-native';
import * as SecureStore from 'expo-secure-store';
import { useIsFocused } from '@react-navigation/native';
import React, { useState, useEffect,useCallback } from 'react';
import { FlatList } from 'react-native-gesture-handler';
import { api_url } from '../../authentication';
import LineChartScreen from "reactnative/screens/charts/LineChart.js";
import { ScrollView, Dimensions, Button, TouchableHighlight, Alert } from 'react-native';
import {Table, Row, Rows,TableWrapper,Cell} from 'react-native-table-component';
import { auth_delete } from '../../authentication';
import { auth_get } from '../../authentication';
import { useTheme } from "reactnative/src/theme/ThemeProvider";
import { styles } from "reactnative/screens/All_Styles.style.js";
import SwitchSelector from "react-native-switch-selector";
import ConditionalModal from '../Modal';
import Loading from '../banking/Loading';
import { ConvertTransactionsToGraphCompatibleData } from '../helper';


// Define a component that takes in a route and navigator to display information about a chosen account
export default function StockAsset({ route, navigation, }){
  const [stocks, setStocks] = useState()
  const {dark, colors, setScheme } = useTheme();
  const [loading, setLoading] = useState(true);
  const [graph, setGraph] = useState({})

  const stylesInternal = StyleSheet.create({
    buttonContainer: {
      flexDirection: "row",
      justifyContent: "space-between",
      paddingHorizontal: 20,
      marginVertical: 10,
    },
    item:{
      padding: 20,
      borderRadius: 10,
    },
    row:{
      flexDirection: 'row',
      alignItems: 'flex-start',
    },
    name:{
      color: "white",
      fontWeight: 'bold',
      fontSize: 21,
    },
    ins_name:{
      color: "white",
      fontSize: 18,
    },
    timeButton: {
      flex: 1,
      paddingTop: 10,
      paddingBottom: 15,
      paddingHorizontal: 13,
      borderRadius: 4,
    },
    table: {
      flex: 1,
      padding: 10,
      justifyContent: 'center',
      backgroundColor: '#fff',
      paddingTop: 20,
      backgroundColor: colors.background,
    },
    head: {
      height: 44,
       backgroundColor: '#42b983'
    },
    row: { 
      flexDirection: 'row',
      justifyContent: 'center',
    },
    separator: {
      height: 1,
      backgroundColor: "#3f3f46",
    },
    balanceContainer: {
      flexDirection: 'row',
      alignSelf: 'center',
      // alignItems: 'center',
      // justifyContent: 'center',
      // marginTop: 20,
    },
    balanceText: {
      fontSize: 21,
      fontWeight: 'bold',
      // marginHorizontal: 20,
      color: colors.text,
    },
    centeredView: {
      flex: 1,
      justifyContent: 'center',
      alignItems: 'center',
      marginTop: 22,
    },
  });

  
// Define a function called getStocks that takes an account ID parameter.
  const getStocks = useCallback(async (accountID) => {
      try {
        const res = await fetch(api_url + `/stocks/list_stocks/${accountID}/`, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${await SecureStore.getItemAsync("token")}`,
          },
        });
        // If the response status is 200 OK, set the stocks state variable to the response data and setLoading to false.
        if(res.status == 200){
          
          const data = await res.json();
          setStocks(data);
          setLoading(false);
        }

      } catch (error) {
        console.error(error);
      }
  });
  // Use the useEffect hook to call getStocks whenever the screen is focused and the account ID parameter changes.
  useEffect(() => {
    if (useIsFocused ) {
      getStocks(route.params.accountID);
    }
  }, [isFocused]);


  const isFocused = useIsFocused();
  const [transactions, setTransactions] = useState(route.params.transactions);

  const deleteAccount = async () => {
    await auth_delete(`/stocks/delete_account/${route.params.accountID}/`)
  }
    
// Define a variable called transaction_table_data that will be an array of arrays,
// where each inner array contains the ID, amount, date, quantity, and fees for a single transaction.
  const transaction_table_data = transactions
    ? transactions.map((item) => [
        item.id,
        (item.amount).toFixed(2), 
        item.date, 
        item.quantity, 
        item.fees,
      ])
    : null;
  // Define an object called tableData that is used to display table data
  const tableData = {
    tableHead: ['ID','Amount', 'Date', 'Quantity','Fees'],
    tableData : transaction_table_data
  };
  

  const [data, setTableData] = React.useState(tableData);
  const [showTable,setShowTable] = React.useState(false);
  const [showStocks,setShowStocks] = React.useState(false);
  
  const {width: SIZE} = Dimensions.get('window');

  // Define a function called toggleTable that is used to toggle table from view.
  const toggleTable = () => {
    setShowTable(!showTable);
  };
  // Define a function called toggleStocksView that is used to toggle stock list from view.
  const toggleStocksView = () => {
    setShowStocks(!showStocks);
  };

  const filter_transactions = (time) => {
    const currentDate = new Date();
    const currentDateTime = currentDate.getTime();

     // Calculate the date and time of the last transaction based on the time parameter.
    const lastTransactionDate = new Date(currentDate.setDate(currentDate.getDate() - time));
    const lastTransactionDateTime = lastTransactionDate.getTime();
  
    // Filter the transaction data to include only transactions that occurred within the last "time" frame.
    let updated_data = route.params.transactions.filter(transaction => {
      const transactionDateTime = new Date(transaction.date).getTime();

      if (transactionDateTime <= currentDateTime && transactionDateTime > lastTransactionDateTime) {
        return true;
      }
      return false;
    })

    // Format the updated transaction data in a table compatible format.
    let updated_table_data = updated_data.map((item) => [
        item.id,
        (item.amount).toFixed(2), 
        item.date, 
        item.quantity, 
        item.fees,
    ]);

    // Update the state variables for tableData and transactions with the updated data.
    setTableData({
        tableHead: ['ID','Amount', 'Date', 'Quantity','Fees'],
        tableData : updated_table_data,
    });
    setTransactions(updated_data);
  }

  const last_week = () => {
    filter_transactions(7);
  }

  const last_month = () => {
    filter_transactions(30);
  }

  const last_year = () => {
    filter_transactions(365);
  }

  const all_time = () => {
    setTransactions(route.params.transactions);
    setTableData(tableData);
  }

  const [graphVersion,setGraphVersion] = React.useState(1);
  const [modalVisible, setModalVisible] = useState(false);

  // Define a useEffect hook that is triggered whenever the value of the "transactions" prop changes.
   useEffect(() => {
      // Map transaction data into an array of {timestamp, value} format so that it can be used to feed the line chart with data.
      let transformedData = ConvertTransactionsToGraphCompatibleData(transactions, route.params.balance);
      
      // Set the state variable "graph" to the transformed data.
      setGraph(transformedData);
    }, [transactions]);

  if(loading){
    return(<Loading/>)
  }
  else{
    return(
      <FlatList
        style={[styles(dark, colors).container]}
        data={transactions}
        keyExtractor={(item) => item.id.toString()}
        ListHeaderComponent={
          <View style={styles(dark, colors).container}>
            <View style={stylesInternal.balanceContainer}>
              <Text style={[{fontSize: 13, fontWeight: 'bold',color: colors.text}]}>{route.params.name} • {route.params.balance_currency} • {route.params.account_name}</Text>
            </View>
            
            <View style={{flexDirection: 'row', alignItems: 'center',paddingHorizontal: 30,paddingBottom:13}}>

            <View style={{flexDirection: 'row', alignItems: 'center'}}>
              <View style={{flexDirection: 'row', alignItems: 'center'}}>
                <Text style={stylesInternal.balanceText}>BALANCE:  </Text>
                <Text style={stylesInternal.balanceText}>£{route.params.balance}</Text>
              </View>
              
              <View style={{flex: 1, alignItems: 'flex-end'}}>
                {route.params.logo !== null && 
                  <Image
                    style={{ width: 60, height: 60 }}
                    source={{ uri: `data:image/png;base64,${route.params.logo}` }}
                  />
                }
                {route.params.logo === null && 
                  <Image
                    style={{ width: 60, height: 60 }}
                    source={{ uri: 'https://kriptomat.io/wp-content/uploads/t_hub/usdc-x2.png' }}
                  />
                }
              </View>
            </View>



          </View>
          
          <View style={{paddingHorizontal: 40,paddingBottom: 20}}>
            <SwitchSelector
              initial={0}
              onPress={value => setGraphVersion(value)}
              selectedColor="#fff"
              buttonColor="#7a44cf"
              borderColor="#7a44cf"
              hasPadding
              options={[    
                { label: "Line Chart", value: 1},  
                { label: "Candlestick Chart", value: 3} 
              ]}
              textStyle={{ fontWeight: 'bold' }}
            />
          </View>


          {transactions && 
            <LineChartScreen 
              data={graph}
              current_balance={route.params.balance}
              graph_version={graphVersion}
              height={275}
              width={SIZE}
          />}
          
          <View style={stylesInternal.buttonContainer, {flexDirection: "row", paddingHorizontal: 10}}>
            <View style={stylesInternal.timeButton}><Button onPress={all_time} title="ALL"/></View>
            <View style={stylesInternal.timeButton}><Button onPress={last_year} title="Y"/></View>
            <View style={stylesInternal.timeButton}><Button onPress={last_month} title="M"/></View>
            <View style={stylesInternal.timeButton}><Button onPress={last_week} title="D"/></View>
          </View>

          <View style={{padding: 20}}>

            <Button
                onPress={toggleTable}
                title={showTable ? "Hide Transactions" : "View Transactions"}
                color="#fcd34d"
            />

            {showTable && (
                <View style={stylesInternal.table}>
                    {data.tableData.length > 0 ? (
                      <View>
                        <Text style={[{textAlign: 'center', alignSelf: 'center', color: colors.text}]}>Press on any transaction to view in depth details.{"\n"}</Text>
                        
                        <Table borderStyle={{ borderWidth: 2, borderColor: '#42b983' }}>
                          <Row data={data.tableHead} style={stylesInternal.head} />
                          {data.tableData.map((rowData, index) => (
                            <TouchableOpacity key={index} onPress={() => navigation.navigate('TransactionData', { id: rowData[0] })}>
                              <TableWrapper style={[stylesInternal.row, {backgroundColor: rowData[1] < 0 ? "#f87171" : '#bbf7d0'}]} borderStyle={{borderWidth: 1, borderColor: '#000000'}}>
                                {rowData.map((cellData, cellIndex) => (
                                  <Cell key={cellIndex} data={cellData} textStyle={{textAlign: 'center', fontSize: 12}} />
                                ))}
                              </TableWrapper>
                            </TouchableOpacity>
                          ))}
                        </Table>

                      </View>
                    ) : (
                      <Text style={[{textAlign: 'center', alignSelf: 'center', color: colors.text}]}>{'\n'}No transaction data available.</Text>
                    )}
                </View>
            )}
            
            <Button
              onPress={toggleStocksView}
              title={showStocks ? "Hide Stocks" : "View Stocks"}
              color="#fcd34d"
            />
            
            {showStocks &&  (
              <FlatList 
                data={stocks} 
                style={{paddingVertical: 5, paddingHorizontal: 10}}
                ItemSeparatorComponent={() => <View style={{height: 5}} />}
                contentContainerStyle={{paddingBottom: 20}}
                renderItem={({item, index}) =>{
                  return (
                    <TouchableOpacity style={[stylesInternal.item, {backgroundColor: colors.primary}]} onPress={()=> navigation.navigate('StockDetails', {stock: stocks[index], security_id: stocks[index].security_id}) }>
                    <View style={stylesInternal.row}>
                      <Text style={[stylesInternal.name, {fontSize: 14}]}> {item.name} </Text>
                    </View>
                  </TouchableOpacity>
                  )
                }}
                ListEmptyComponent={<Text style={[{textAlign: 'center', alignSelf: 'center', color: colors.text}]}>{'\n'}No stock data available.</Text>}
                />)
              }

              <View style={{marginTop: 40}}>
                <Button title="REMOVE" color="red" onPress={() => setModalVisible(true)}/>
              </View>

              <ConditionalModal
                headerText={"Remove Your Account"}
                bodyText={"Are you sure you want to remove your account?"}
                visible={modalVisible}
                onEvent={async () => {await deleteAccount(), navigation.goBack()}}
                onClose={() => setModalVisible(false)}
              />

          </View>
        </View>
        }
      />
    );
      }
}