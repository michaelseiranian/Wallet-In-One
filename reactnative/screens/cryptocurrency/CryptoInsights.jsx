import {View, Text, StyleSheet, Image, ScrollView, Dimensions} from "react-native";
import React, {useEffect, useState} from "react";
import { useTheme } from '../../src/theme/ThemeProvider'
import { BACKEND_URL } from "@env"
import * as SecureStore from "expo-secure-store";
import getCryptoIcon from "./icons/icon";
import { LineChart } from 'react-native-chart-kit';

/**
 * Component that displays crypto insights for both wallets and exchanges, including insights for predicted balance,
 * total spend and received, average spend for crypto wallets, and most expensive transaction and a chart of monthly
 * transactions for crypto exchanges.
 */
export default function CryptoInsights() {
  const [insights, setInsights] = useState({predicted_balance: {}, received_spent: {}, average_spend: {}});
  const [exchangeInsights, setExchangeInsights] = useState({all_transactions: {}, most_expensive_transaction: {}});
  const {dark, colors, setScheme} = useTheme();
  const [ graphData, setGraphData ] = useState(null);
  const {width: SIZE} = Dimensions.get('window');

  const styles = StyleSheet.create({
    title: {
      fontWeight: "900",
      fontSize: 40,
      alignSelf: "center",
      paddingVertical: 10,
      color: colors.text
    },
    subtitle: {
      fontWeight: "900",
      fontSize: 30,
      alignSelf: "center",
      color: colors.text
    },
    smallSubtitle: {
      fontWeight: "900",
      fontSize: 24,
      alignSelf: "center",
      color: colors.text,
      textAlign: 'center',
    },
    info: {
      fontWeight: "900",
      fontSize: 15,
      alignSelf: "center",
      color: colors.text
    }
  });

  useEffect(() => {
    fetchInsights();
    fetchExchangeInsights();
  }, [])

  /**
   * Function that fetches the crypto wallet insights from the backend according to the requesting user.
   */
  const fetchInsights = async () => {
    await fetch(`${BACKEND_URL}/crypto_wallets/insights`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Token ${await SecureStore.getItemAsync("token")}`,
      },
    })
      .then((res) => res.json())
      .then((res) => setInsights(res))
      .catch((err) => console.log(err));
  };

  /**
   * Function that fetches the crypto exchange insights from the backend according to the requesting user.
   */
  const fetchExchangeInsights = async () => {
    await fetch(`${BACKEND_URL}/crypto-exchanges/get_insights/`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Token ${await SecureStore.getItemAsync("token")}`,
      },
    })
      .then((res) => res.json())
      .then((res) => {
        setExchangeInsights(res);
  
        const transactions = res.all_transactions;
  
        if (transactions.length === 1 && transactions[0] === "empty") {
          setGraphData("empty");
        } else {
          // Group transactions by month
          const transactionsByMonth = transactions.reduce((acc, transaction) => {
            const month = transaction.timestamp.slice(0, 7);
            acc[month] = acc[month] || [];
            acc[month].push(transaction);
            return acc;
          }, {});
  
          // Calculate the number of transactions for each month
          const labels = Object.keys(transactionsByMonth);
          const values = labels.map((month) => transactionsByMonth[month].length);
          const numDataPoints = labels.length;
          const step = Math.ceil(numDataPoints / 4);
          const filteredLabels = labels.filter((_, index) => index % step === 0);
          const chartData = {
            labels: filteredLabels,
            datasets: [
              {
                data: values,
              },
            ],
          };
          setGraphData(chartData);
        }
      })
      .catch((err) => console.log(err));
  };  

  const chartConfig = {
    backgroundGradientFrom: colors.background,
    backgroundGradientTo: colors.background,
    color: () => colors.text,
    strokeWidth: 3,
    xAxisLabel: "",
    xAxisInterval: 5,
  };

  return (
    <ScrollView style={{ flex: 1, backgroundColor: colors.background, paddingHorizontal: 20 }}>
      <Text />

      <Text style={styles.smallSubtitle}>Predicted Balance in Crypto Wallets</Text>
      <Text style={styles.info}>Next four weeks</Text>
      <View style={{ borderRadius: 10, paddingVertical: 10}}>
        {
          Object.keys(insights.predicted_balance).length === 0
            ?
            <Text style={{color: colors.text}}>There are no wallet insights to display. Try connect a crypto wallet.</Text>
            :
            <View>
              {
                Object.entries(insights.predicted_balance).map(([key, value]) =>
                  <InsightItem key={key} symbol={key} upper={value} />
                )
              }
            </View>
        }
      </View>
      <Text />

      <Text style={styles.smallSubtitle}>Total Spent & Received in Crypto Wallets</Text>
      <View style={{ borderRadius: 10, paddingVertical: 10}}>
        {
          Object.keys(insights.received_spent).length === 0
            ?
            <Text style={{color: colors.text}}>There are no wallet insights to display. Try connect a crypto wallet.</Text>
            :
            <View>
              {
                Object.entries(insights.received_spent).map(([key, value]) =>
                  <InsightItem key={key} symbol={key} upper={`+${value.received}`} lower={`-${value.spent} ${key}`} />
                )
              }
            </View>
        }
      </View>
      <Text />

      <Text style={styles.smallSubtitle}>Average Spend in Crypto Wallets</Text>
      <View style={{ borderRadius: 10, paddingVertical: 10}}>
        {
          Object.keys(insights.average_spend).length === 0
            ?
            <Text style={{color: colors.text}}>There are no wallet insights to display. Try connect a crypto wallet.</Text>
            :
            <View>
              {
                Object.entries(insights.average_spend).map(([key, value]) =>
                  <InsightItem key={key} symbol={key} upper={`${value * -1}`} />
                )
              }
            </View>
        }
      </View>
      <Text />

      <Text style={styles.smallSubtitle}>Most Expensive Transaction in Crypto Exchanges</Text>
      <View style={{ borderRadius: 10, paddingVertical: 10}}>
        {exchangeInsights ? (
          exchangeInsights.most_expensive_transaction[0] !== "empty" ? (
            <InsightItem symbol={exchangeInsights.most_expensive_transaction[5]} upper={`${exchangeInsights.most_expensive_transaction[1]} ${exchangeInsights.most_expensive_transaction[0]} (£${exchangeInsights.most_expensive_transaction[2]}), type: ${exchangeInsights.most_expensive_transaction[3]}`} lower={`${exchangeInsights.most_expensive_transaction[4]}`}/>
          ) : (
            <Text style={{color: colors.text}}>There are no transactions in your cryptocurrency exchanges.</Text>
          )
        ) : (
          <Text style={{color: colors.text}}>Loading...</Text>
        )}
      </View>
      <Text />

      <Text style={styles.smallSubtitle}>Number of Monthly Transactions in Crypto Exchanges</Text>
      <View style={{ borderRadius: 10, paddingVertical: 10}}>
        {graphData ? (
          graphData === "empty" ? (
            <Text style={{color: colors.text}}>There is no transaction data from crypto exchanges.</Text>
          ) : (
            <LineChart
              data={graphData}
              width={SIZE}
              height={SIZE/1.8}
              chartConfig={chartConfig}
              bezier
              style={{ marginTop: 10, marginLeft: -20 }}
            />
          )
        ) : (
          <Text style={styles.smallSubtitle}>Loading...</Text>
        )}
      </View>

    </ScrollView>
  )
}

/**
 * Component that formats each insight item displaying each of the values, the associated cryptocurrency and the icon.
 */
function InsightItem(props) {

  const {dark, colors, setScheme} = useTheme();
  const [value, setValue] = useState(0);

  /**
   * Function that gets the conversion rate of the target cryptocurrency into pounds and stores it in the component.
   */
  const getCryptoValue = async () => {
    await fetch(`https://min-api.cryptocompare.com/data/price?fsym=${props.symbol}&tsyms=GBP`)
      .then((res) => res.json())
      .then((res) => res.GBP)
      .then((res) => setValue(res))
      .catch((err) => console.log(err))
  }

  useEffect(() => {
    getCryptoValue()
  }, [])

  const styles = StyleSheet.create({
    walletAsset: {
      paddingHorizontal: 10,
      borderRadius: 10,
      flexDirection: "row",
    },
    walletAssetTitle: {
      fontWeight: "700",
    },
    walletAssetImage: {
      width: 30,
      height: 30,
    },
  });

  return (
    <View style={[styles.walletAsset, {paddingVertical: 5}]}>
      <View
        style={{
          alignItems: "center",
          justifyContent: "center",
          paddingRight: 10,
        }}
      >
        <Image
          style={styles.walletAssetImage}
          source={getCryptoIcon(props.symbol)}
        />
      </View>

      <View
        style={{
          flex: 1,
          flexDirection: "row",
          justifyContent: "space-between",
        }}
      >
        <View>
          <Text style={{ fontSize: 20, fontWeight: "700", color: colors.text }}>
            {props.symbol}
          </Text>

          <Text style={[styles.walletAssetTitle, {color: colors.text}]}>
            {props.upper} {props.symbol}
          </Text>

          {
            props.lower
              ?
              <Text style={[styles.walletAssetTitle, {color: colors.text}]}>
                {props.lower}
              </Text>
              :
              <Text style={[styles.walletAssetTitle, {color: colors.text}]}>
                £{value * props.upper} {props.symbol}
              </Text>
          }

        </View>

      </View>
    </View>
  );
}