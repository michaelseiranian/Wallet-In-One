import React, { useEffect, useState } from 'react';
import { StyleSheet, Text, ScrollView, Dimensions, View, TouchableOpacity } from 'react-native';
import { VictoryChart, VictoryBar, VictoryLabel, VictoryAxis, VictoryStack } from "victory-native";


import fixture from "../../charts/chartData.json"
import { useTheme } from 'reactnative/src/theme/ThemeProvider'
import { Alert } from "react-native"

export default function StackedChart({ data = fixture.all, handlePressIn  }) {
  const {dark, colors, setScheme} = useTheme();
  return (
    <ScrollView
      contentContainerStyle={{
        flexGrow : 1,
        justifyContent: 'center',
        alignItems: 'center',
        paddingBottom: 20,
        backgroundColor: colors.background,
      }}
      style={styles.container}
    >
      {/*domain={{ x: [1, 4] }}*/}
      <VictoryChart  domainPadding={{ x: 20, y: 20 }} >
        <VictoryAxis
          dependentAxis
           style={{
               axis: {stroke: 'grey'},
            tickLabels: {fill: colors.text , fontSize: 12},
             grid: {stroke: 'grey'},
           }}
        />
        <VictoryAxis
          tickValues={[ 1, 2, 3, 4 ,5]}
          style={{
            axis: {stroke: 'grey'},
            tickLabels: {fill: colors.text},
          }}
        />
        <VictoryStack colorScale={["tomato", "orange", "gold", "purple"]} >
          {/* style={{data: {stoke: 'black', strokeWidth: 3}}}> */}
          {(data['Banks']?data['Banks']:[]).map(i => (
            <VictoryBar
              key={i}
              data={[{ x: "Banks", y: i.y, z: i.x, name: "Banks" }]}
              barWidth={35}
              events={[
                {
                  target: "data",
                  eventHandlers: {
                    onPressIn: handlePressIn,
                  },
                },
              ]}
            />
          ))}
          {(data['Cryptocurrency from wallets']?data['Cryptocurrency from wallets']:[]).map(i => (
            <VictoryBar
              key={i}
              data={[{ x: "Crypto\nWallets ", y: i.y, z: i.x, name: "Cryptocurrency from wallets" }]}
              barWidth={35}
              events={[
                {
                  target: "data",
                  eventHandlers: {
                    onPressIn: handlePressIn,
                  },
                },
              ]}
            />
          ))}
          {(data['Cryptocurrency from exchanges']?data['Cryptocurrency from exchanges']:[]).map(i => (
            <VictoryBar
              key={i}
              data={[{ x: "Crypto\nExchanges", y: i.y, z: i.x, name: "Cryptocurrency from exchanges" }]}
              barWidth={35}
              events={[
                {
                  target: "data",
                  eventHandlers: {
                    onPressIn: handlePressIn,
                  },
                },
              ]}
            />
          ))}
          {(data['Stock Accounts']?data['Stock Accounts']:[]).map(i => (
            <VictoryBar
              key={i}
              data={[{ x: "Stocks", y: i.y, z: i.x, name: "Stock Accounts"}]}
              barWidth={35}
              events={[
                {
                  target: "data",
                  eventHandlers: {
                    onPressIn: handlePressIn,
                  },
                },
              ]}
            />
          ))}
        </VictoryStack>
      </VictoryChart>


    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  title: {
    fontWeight: '900',
    fontSize: 50,
    alignSelf: 'center',
    paddingVertical: 10,
  },
  button: {
    width: "75%",
    borderRadius: 25,
    textAlign: 'center',
    fontWeight: 'bold',
    fontSize:  30,
  },
});
