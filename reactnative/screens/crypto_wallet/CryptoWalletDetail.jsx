import {
  Dimensions,
  Image,
  Pressable,
  StyleSheet,
  Text,
  View,
  ScrollView,
  FlatList
} from "react-native";
import React, {useEffect, useState} from "react";
import getCryptoIcon from "../cryptocurrency/icons/icon";
import { useTheme } from '../../src/theme/ThemeProvider';
import {styles} from '../All_Styles.style.js';
import * as SecureStore from "expo-secure-store";
import { BACKEND_URL } from "@env"
import LineChartScreen from "../charts/LineChart";
import SwitchSelector from "react-native-switch-selector";
import ConditionalModal from "../Modal";

/**
 * Component that display detailed data on a crypto wallet, displaying the address, its balance and spend/received
 * count, along with a list of transactions and a line chart with a candlestick chart of its price fluctuations over time.
 */
export default function CryptoWalletDetail(props) {

  const {dark, colors, setScheme} = useTheme();
  const { id, item, value, removeWallet } = props.route.params;
  const [ walletData, setWalletData ] = useState({transactions:[]})
  const [ graphData, setGraphData ] = useState([{timestamp: 0, value: 0}, {timestamp: 0, value: 0}]);
  const [ loading, setLoading ] = useState(true);
  const [ chartType, setChartType ] = useState("breakdown");
  const [modalVisible, setModalVisible] = useState(false);
  const {width: SIZE} = Dimensions.get('window');
  const [graphVersion, setGraphVersion] = useState(4);

  /**
   * Function that retrieves the detailed wallet data from the backend using the id of the wallet.
   */
  const retrieveWallet = async (id) => {
    await fetch(`${BACKEND_URL}/crypto_wallets/${id}/`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Token ${await SecureStore.getItemAsync("token")}`,
      },
    })
      .then((res) => res.json())
      .then((res) => setWalletData(res))
      .catch((err) => console.log(err));
  };

  /**
   * Function that converts the transaction data of a wallet using the timestamp and value into a form that can be used
   * to display the balance history for the graphs.
   */
  const convertData = () => {
    let points = [];
    let balance = walletData.balance;

    for (let i = 0; i < walletData.transactions.length; i++) {
      let point = {timestamp: walletData.transactions[i].time * 1000, value: balance}
      balance -= walletData.transactions[i].value
      points = [point, ...points]
    }
    setGraphData(points)
  }

  /**
   * Function that handles the chart change from the options of a line chart or a candlestick chart.
   */
  const handleChartTypeChange = (type) => {
    setChartType(type);
  };

  useEffect(() => {
    retrieveWallet(id)
    }, []);

  useEffect(() => {
    convertData()
    setLoading(false)
  }, [walletData]);

  const stylesInternal = StyleSheet.create({
    walletAsset: {
      borderRadius: 10,
      padding: 20,
    },
    walletAssetImage: {
      width: 100,
      height: 100,
    },
    mediumBoldText: {
      fontWeight:"800",
      fontSize:25,
      paddingTop: 10,
      color: colors.text,
    }
  });

  return (
    <View style={{flex: 1, backgroundColor: colors.background}}>

      <Text />
      <Text />
      <View style={{paddingHorizontal: 30}}>
        <Image
          style={stylesInternal.walletAssetImage}
          source={getCryptoIcon(walletData.symbol)}
        />
        <Text style={styles(dark, colors).largeTextBold}>{walletData.cryptocurrency} Wallet</Text>
      </View>

      <View style={{paddingHorizontal: 40,paddingVertical:20}}>
        <SwitchSelector
          initial={0}
          onPress={value => handleChartTypeChange(value)}
          selectedColor="#fff"
          buttonColor="#7a44cf"
          borderColor="#7a44cf"
          hasPadding
          options={[    
            { label: "Breakdown", value: "breakdown"},  
            { label: "Transactions", value: "transactions"} 
          ]}
          textStyle={{ fontWeight: 'bold', fontSize: 15 }}
          buttonMargin={1}
          height={45}
        />
      </View>

      {
        chartType === "breakdown" ?
          <ScrollView>
            <View style={{paddingHorizontal: 30}}>

              <Text style={{fontWeight:"800", fontSize:25, paddingTop: 10, color: colors.text}}>Breakdown</Text>
              <Text />

              <Text style={styles(dark, colors).textBold}>Address</Text>
              <Text style={styles(dark, colors).text}>{walletData.address}</Text>
              <Text />

              <Text style={{fontWeight: "700", color: colors.text}}>Balance</Text>
              <Text style={{color: colors.text}}>{walletData.balance} {walletData.symbol}</Text>
              <Text />

              <Text style={{fontWeight: "700", color: colors.text}}>Value</Text>
              <Text style={{color: colors.text}}>£{value.toFixed(2)}</Text>
              <Text />

              <Text style={{fontWeight: "700", color: colors.text}}>Received</Text>
              <Text style={{color: colors.text}}>{walletData.received} {walletData.symbol}</Text>
              <Text />

              <Text style={{fontWeight: "700", color: colors.text}}>Spent</Text>
              <Text style={{color: colors.text}}>{walletData.spent} {walletData.symbol}</Text>
              <Text />

              <Text style={{fontWeight: "700", color: colors.text}}>Output Count</Text>
              <Text style={{color: colors.text}}>{walletData.output_count}</Text>
              <Text />

              <Text style={{fontWeight: "700", color: colors.text}}>Unspent Output Count</Text>
              <Text style={{color: colors.text}}>{walletData.unspent_output_count}</Text>

            </View>

            <Pressable
              onPress={() => setModalVisible(true)}
              style={{alignItems: "center", justifyContent: "center"}}>
              <View style={styles(dark, colors).smallButton}>
                <Text style={{color: colors.text, fontWeight: "800"}}>Remove</Text>
              </View>
            </Pressable>

            <ConditionalModal
              headerText={"Remove Your Wallet"}
              bodyText={"Are you sure you want to remove your wallet account?"}
              visible={modalVisible}
              onEvent={() => removeWallet(walletData.id).then(() => props.navigation.goBack())}
              onClose={() => setModalVisible(false)}
            />

            <Text style={{fontWeight:"800", fontSize:25, paddingTop: 10,paddingHorizontal:30, color: colors.text}}>Balance History Graph</Text>
            <View>
              {
                graphData.length <= 2 ?
                  <Text style={{color: colors.text,paddingHorizontal:30}}>Not enough data to display graph.</Text>
                  :
                  <View style={[styles.walletAsset, {backgroundColor: colors.background,paddingBottom:30}]}>

                    <View style={{padding: 15,paddingHorizontal: 45}}>
                      <SwitchSelector
                        initial={0}
                        onPress={value => setGraphVersion(value)}
                        selectedColor="#fff"
                        buttonColor="#7a44cf"
                        borderColor="#7a44cf"
                        hasPadding
                        options={[
                          { label: "Line Chart", value: 4},
                          { label: "Candlestick Chart", value: 3}
                        ]}
                        imageStyle={{ width: 20, height: 20 }}
                        textStyle={{ fontWeight: 'bold' }}
                      />
                    </View>

                    {graphData &&
                      <LineChartScreen
                        transactions={null}
                        current_balance={graphData[graphData.length-1].value}
                        graph_version={graphVersion}
                        height={SIZE / 2}
                        width={SIZE}
                        data={graphData}
                      />}

                  </View>
              }
            </View>

          </ScrollView>
          :
          <View style={{paddingHorizontal: 30}}>
            <Text style={{fontWeight:"800", fontSize:25, paddingTop: 10, color: colors.text}}>Transactions</Text>
            <View style={[styles.walletAsset, {backgroundColor: colors.background}]}>

              {walletData.transactions.length === 0
                ?
                <Text style={{color: colors.text}}>There are no transactions to display.</Text>
                :
                <FlatList
                  data={walletData.transactions}
                  renderItem={(t) => <CryptoWalletTransaction key={t.id} transaction={t} symbol={walletData.symbol}/> }
                />
              }

            </View>
          </View>
      }

    </View>
  );

}

/**
 * Component that displays a transaction from a list, showing the value of the transaction and the date that the
 * transaction happened.
 */
function CryptoWalletTransaction(props) {

  const {dark, colors, setScheme} = useTheme();
  const date_options = {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: 'numeric',
    minute: 'numeric'
  };

  const raw_date = new Date(Number(props.transaction.item.time * 1000))
  const formatted_date = raw_date.toLocaleString("en-JP", date_options);

  return (
    <View style={styles.transaction}>
      <Text />
      <Text style={{color: colors.text, fontWeight: "700", fontSize: 16}}>{props.transaction.item.value} {props.symbol}</Text>
      <Text style={{color: colors.text}}>{formatted_date}</Text>
    </View>
  )
}
