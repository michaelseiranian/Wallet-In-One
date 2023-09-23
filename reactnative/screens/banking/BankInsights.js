import { View, ScrollView, Text, StyleSheet, Button } from 'react-native';
import { useTheme } from 'reactnative/src/theme/ThemeProvider'
import { useState, useEffect } from 'react';
import { useIsFocused } from '@react-navigation/native';
import Loading from './Loading'
import { auth_get } from '../../authentication'
import { BalanceChart } from './BalanceChart'
import { BankBarChart } from './BankBarChart'
import {styles} from 'reactnative/screens/All_Styles.style.js'

import { BankBarChart2 } from './BankBarChart'

const SegmentedControl = ({ segments, activeIndex, setActiveIndex }) => {
  return (
    <View style={stylesInternal.segmentContainer}>
      {segments.map((segment, index) => (
        <View style={stylesInternal.buttonContainer} key={index}>
          <Button
            title={segment}
            color={activeIndex === index ? '#007AFF' : 'grey'}
            onPress={() => setActiveIndex(index)}
          />
        </View>
      ))}
    </View>
  );
};

const stylesInternal = StyleSheet.create({
  segmentContainer: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    //backgroundColor: '#f2f2f2',
    borderRadius: 4,
    overflow: 'hidden',
  },
  buttonContainer:{
    marginHorizontal: 10,
  },
  columnCenter:{
    flexDirection: 'column', alignItems: 'center'
  },
  item:{
    marginVertical:10,
  }
});


export default function BankInsights() {
  const [ isLoading, setIsLoading ] = useState(true)
  const isFocused = useIsFocused();
  const { dark, colors, setScheme} = useTheme();

  const [activeIndex, setActiveIndex] = useState(0);
  const [activeTab, setActiveTab ] = useState(0)

  const [ data, setData ] = useState('None')
  const [ currentData, setCurrentData ] = useState()
  const [ currentTabData, setCurrentTabData ] = useState()
  
  useEffect(() =>{
    const fetchData = async () => {
      response = await auth_get('/banking/metrics/')
        
        if (response.status == 200){
            setData(response.body)
            setCurrentData(response.body.all)
            setCurrentTabData(response.body.all.both)
            setActiveIndex(0)
            setActiveTab(0)
            setIsLoading(false)
        }
    }
    if (isFocused != false){fetchData()}
  }, [isFocused])


  useEffect(() =>{
    console.log(activeIndex)
    switch(activeIndex){
      case 0:
        setCurrentData(data['all'])
        break
      case 1:
        setCurrentData(data['1month'])
        break
      case 2:
        setCurrentData(data['3month'])
        break
      case 3:
        setCurrentData(data['6month'])
        break
    }
  }, [activeIndex])

  useEffect(() =>{
    if(currentData){
      switch(activeTab){
        case 0:
          setCurrentTabData(currentData['both'])
          break
        case 1:
          setCurrentTabData(currentData['positive'])
          break
        case 2:
          setCurrentTabData(currentData['negative'])
          break
      }
    }
  }, [activeTab, currentData])

  if (isLoading){
    return <Loading/>
  }

  return (
    <ScrollView>
    <View style={[ styles(dark, colors).container, {justifyContent: 'flex-start', alignItems: 'center', marginBottom: 100 }]}>
      <View style={stylesInternal.item}>
        <SegmentedControl segments={['All', '1 Month','3 Month', '6 Month']} activeIndex={activeIndex} setActiveIndex={setActiveIndex} />
      </View>
      
      <View style={stylesInternal.item}>
        <View style={{ width: "80%", flexDirection: 'row', justifyContent: 'space-evenly' }}>
        <View style={stylesInternal.columnCenter}>
            <Text style={styles(dark, colors).textBold}>Money In:</Text>
            <Text style={{ color: 'green' }} >£{currentData.total_money_in}</Text>
          </View>
          <View style={stylesInternal.columnCenter}>
            <Text style={styles(dark, colors).textBold}>Money Out:</Text>
            <Text style={{ color: 'red' }} >£{currentData.total_money_out}</Text>
          </View>
          <View style={stylesInternal.columnCenter}>
            <Text style={styles(dark, colors).textBold}>Net:</Text>
            <Text style={{ color: currentData.net>0?'green':'red' }} >£{currentData.net}</Text>
          </View>
        </View>
      </View>
      <Text style={styles(dark, colors).text}>Balance History:</Text>
      <BalanceChart rawData={currentData.balance_history} highest={currentData.highest_balance}/>

      <Text style={styles(dark, colors).text}> Highest Balance: £{currentData['highest_balance'].toFixed(2)}</Text>
      <Text style={styles(dark, colors).text}> Lowest Balance: £{currentData['lowest_balance'].toFixed(2)}</Text>

      <View style={stylesInternal.item}>
        <SegmentedControl segments={['Both', 'Income','Spending']} activeIndex={activeTab} setActiveIndex={setActiveTab} />
      </View>

      <Text style={styles(dark, colors).text}> Number of Transactions: {currentTabData['total_amount_of_transactions']}</Text>
      <Text style={styles(dark, colors).text}> Highest Transaction: £{currentTabData['highest_transaction'].toFixed(2)}</Text>
      <Text style={styles(dark, colors).text}> Lowest Transaction: £{currentTabData['lowest_transaction'].toFixed(2)}</Text>
      <Text style={styles(dark, colors).text}> Average Transaction: £{currentTabData['average_transaction'].toFixed(2)}</Text>
      <Text style={styles(dark, colors).text}> Variance: {currentTabData['variance'].toFixed(2)}</Text>
      <Text style={styles(dark, colors).text}> Standard Deviation: {currentTabData['standard_deviation'].toFixed(2)}</Text>
      
      <BankBarChart rawData={currentTabData.bar_data} tab={activeTab}/>
      
    </View>
    </ScrollView>
  );
}
