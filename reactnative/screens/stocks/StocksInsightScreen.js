import {View, Text, StyleSheet, Image, ScrollView, Button} from "react-native";
import React, {useEffect, useState} from "react";
import { useIsFocused } from "@react-navigation/native";
import { auth_get } from "../../authentication";
import Loading from "../banking/Loading";
import Map from "./Map";
import { useTheme } from 'reactnative/src/theme/ThemeProvider';
import { styles } from "reactnative/screens/All_Styles.style.js";
import SwitchSelector from "react-native-switch-selector";

/**
 * Component that displays insights/metrics for all stock accounts currently held by the user.
 */
export default function StockInsight() {
    const {dark, colors, setScheme} = useTheme();
    const isFocused = useIsFocused()
    const [data, setData] = useState()
    const [currentData, setCurrentData] = useState()
    const [isLoading, setIsLoading] = useState(true)
    useEffect( () => {
        const getMetrics = async () => {
        const response = await auth_get('/stocks/get_metrics/')
        if(response.status == 200){
            setData(response.body)
            setCurrentData(response.body.all)
            setIsLoading(false)
        }
        }
        if(useIsFocused){getMetrics()}  
    }, [isFocused])

    /**
     * Function that filters the current data based on the toggle that has currently been set.
     * @param {*} filter 
     */
    const filter = (filter) => {
        setCurrentData(data[filter])
    }

    const stylesInternal = StyleSheet.create({
        button: {
            flexDirection: "row" , justifyContent: 'space-evenly'
        },
        container: {
            padding: 10,
            borderRadius: 5,
            marginVertical: 10,
            shadowColor: '#000',
            shadowOffset: {
                width: 0,
                height: 2,
            },
            shadowOpacity: 0.25,
            shadowRadius: 3.84,
            elevation: 5,
        },
        text: {
            fontSize: 16,
            marginBottom: 5,
        },
    })

    /**
     * Switch Selector, used for filtering the insights based on time.
     */
    const switchButtons = [
        <SwitchSelector
        key={"all"}
        initial={0}
        onPress={value => filter(value)}
        selectedColor="#fff"
        buttonColor="#7a44cf"
        borderColor="#7a44cf"
        hasPadding
        options={[    
          { label: "All", value: "all", testID: "all"},  
          { label: "1 Month", value: "1 Month", testID: "1 Month"},
          { label: "3 Months", value: "3 Months", testID: "3 Months"},
          { label: "6 Months", value: "6 Months", testID: "6 Months"},
          { label: "1 Year", value: "12 Months", testID: "1 Year"}  
        ]}
        imageStyle={{ width: 20, height: 20 }}
        textStyle={{ fontWeight: 'bold', fontSize: 15 }}
        buttonMargin={1}
        height={60}
      />
    ]
    if(isLoading){
        return (<Loading/>)
    }else if(currentData.average_latitude == 0 && currentData.average_longitude == 0){
        return(
        <View style={{flex: 1}}>
            {switchButtons}
            <Text style={[styles(dark, colors).text, {textAlign: 'center'}]}>No Data for Selected Date</Text>
        </View>
        )
    }
    return(
        <View style={styles(dark, colors).container}>
            {switchButtons}
            <View style={stylesInternal.container}>
                <Text style={[stylesInternal.text, styles(dark, colors).textBold, {color: colors.text}]}>Transaction Statistics</Text>
                <Text style={[stylesInternal.text, styles(dark, colors).text]}>Number of Transactions: {currentData.total_number_of_transactions}</Text>
                <Text style={[stylesInternal.text, styles(dark, colors).text]}>Highest Transaction(£): {currentData.highest_transaction}</Text>
                <Text style={[stylesInternal.text, styles(dark, colors).text]}>Lowest Transaction(£): {currentData.lowest_transaction}</Text>
                <Text style={[stylesInternal.text, styles(dark, colors).text]}>Average Transaction(£): {currentData.average_transaction}</Text>
                <Text style={[stylesInternal.text, styles(dark, colors).text]}>Variance: {currentData.variance}</Text>
                <Text style={[stylesInternal.text, styles(dark, colors).text]}>Standard Deviation: {currentData.standard_deviation}</Text>
                <Text style={[stylesInternal.text, styles(dark, colors).text]}>Highest Fee(£): {currentData.highest_fee}</Text>
                <Text style={[stylesInternal.text, styles(dark, colors).text]}>Lowest Fee(£): {currentData.lowest_fee}</Text>
                <Text style={[stylesInternal.text, styles(dark, colors).text]}>Average Fee(£): {currentData.average_fee}</Text>
                <Text style={[stylesInternal.text, styles(dark, colors).text]}>Centroid of Transaction Locations:</Text>
            </View>
            <View style={{flex: 1}}>
                <View style={{height: '100%'}}>
                    <Map latitude={currentData.average_latitude} longitude={currentData.average_longitude}/>
                </View>
            </View>
        </View>
    )
}