import React, { useEffect, useState } from "react";
import {
  StyleSheet,
  Text,
  ScrollView,
  Dimensions,
} from "react-native";

import {
  VictoryPie,
  VictoryLabel,
  VictoryContainer,
} from "victory-native";


import { useTheme } from "reactnative/src/theme/ThemeProvider";

export default function PieChart({colours, data, handlePressIn, labelCount, assetSize, numSize}) {

  const {dark, colors, setScheme} = useTheme();

  if(!colours || !data || !handlePressIn || !labelCount || !assetSize || !numSize){ return null; }

  let value = 0;
  for (let i = 0; i < data.length; i++) {
    value += data[i].y;
  }
  value = value.toFixed(2);

  let assetLabel = 165;
  let numLabel = 185;
  if(labelCount == 2){
    assetLabel = 130;
    numLabel = 180;
  }

  return (
    <ScrollView
      contentContainerStyle={{
        flexGrow: 1,
        justifyContent: "center",
        alignItems: "center",
        //paddingBottom: 20,
        backgroundColor: colors.background,
      }}
      style={styles.container}
    >

      <VictoryContainer
        width={Dimensions.get("window").width}
        // height={Dimensions.get('window').height/2}
        height={300}
        //style={{ paddingBottom: 10 }}
      >
        <VictoryPie
          data={data}
          innerRadius={100}
          padAngle={1}
          cornerRadius={10}
          radius={Dimensions.get("window").width / 3}
          labels={() => null}
          events={[
            {
              target: "data",
              eventHandlers: {
                onPressIn: handlePressIn,
              },
            },
          ]}
          animate={{
            duration: 1000,
            easing: "bounce"
          }}
          colorScale={colours}
          standalone={false}
          height={300}
        />
        <VictoryLabel
          textAnchor="middle"
          style={{ fontSize: assetSize, fill: colors.text }}
          x={Dimensions.get("window").width / 2}
          y={assetLabel}
          text={"Assets"}
        />
        <VictoryLabel
          textAnchor="middle"
          style={{ fontSize: numSize, fontWeight: "700", fill: colors.text }}
          x={Dimensions.get("window").width / 2}
          y={numLabel}
          text={data.length}
        />
          {labelCount === 4 && (
          <>
        <VictoryLabel
          textAnchor="middle"
          style={{ fontSize: 17, fill: colors.text }}
          x={Dimensions.get("window").width / 2}
          y={105}
          text={"Net Worth"}
        />
        <VictoryLabel
          textAnchor="middle"
          style={{ fontSize: 27, fontWeight: "700", fill: colors.text }}
          x={Dimensions.get("window").width / 2}
          y={125}
          text={"£" + value}
        />
                  </>
        )}
      </VictoryContainer>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  button: {
    width: "75%",
    borderRadius: 25,
    textAlign: "center",
    fontWeight: "bold",
    fontSize: 30,
  },
});