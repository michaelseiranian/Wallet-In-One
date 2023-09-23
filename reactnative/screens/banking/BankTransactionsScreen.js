import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View, ScrollView, Button, TextInput, Alert, SectionList , TouchableOpacity, Image } from 'react-native';
import { useState, useEffect } from 'react';
import { auth_get} from '../../authentication'
import { useIsFocused } from '@react-navigation/native';
import Loading from './Loading'
import { useTheme } from 'reactnative/src/theme/ThemeProvider'
import {styles} from 'reactnative/screens/All_Styles.style.js'

function BankTransactionsScreen({ route, navigation }) {
  const [ isLoading, setIsLoading ] = useState(true)
  const [ bankData, setBankData ] = useState([])
  const isFocused = useIsFocused();
  const {dark, colors, setScheme} = useTheme();

  useEffect(() =>{
    const fetchData = async () => {
        console.log('fetch bank transactions')
        setIsLoading(true)
        if (route.params == undefined){
          response = await auth_get('/banking/transactions/')
        }
        else{
          response = await auth_get('/banking/transactions/' + route.params.accountID +'/')
        }
      
        if (response.status == 200){
            console.log(response.body)
            setIsLoading(false)
            response.body.sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp))
            setBankData(response.body)
        }
    }
    if (isFocused != false){fetchData()}
  }, [isFocused])

  const displayDate = (timestamp) => {
    const date = new Date(timestamp);
    return  date.toLocaleDateString();
  };

  const displayTime = (timestamp) => {
    const date = new Date(timestamp);
    return  date.toLocaleTimeString();
  };

  const stylesInternal = StyleSheet.create({
    container: {
      width: '100%',
      paddingBottom: 0,
      borderWidth: 1,
      borderRadius: 5,
      borderColor: dark ? colors.background : '#ddd',
      overflow: 'hidden',
      backgroundColor: colors.background,
    },
    row:{
      flexDirection: 'row',
      alignItems: 'center',
    },
    olditem:{
      padding: 20,
    },
    item: {
      flexDirection: 'row',
      justifyContent: 'space-between',
      alignItems: 'center',
      paddingVertical: 8,
    },
    leftContainer: {
      flex: 1,
    },
    rightContainer: {
      marginLeft: 10,
      alignItems: 'flex-end',
    },
    name: {
      fontWeight: 'bold',
      fontSize: 14,
      color: colors.text,
    },
    date: {
      fontSize: 14,
      color: 'gray',
    },
    amount: {
      fontSize: 16,
      fontWeight: 'bold',
    },
    time: {
      fontSize: 14,
      color: 'gray',
    },
    header:{
      paddingLeft:20, 
      paddingRight: 20,
      paddingTop: 6,
      paddingBottom: 6,
      fontWeight: 'bold',
      color:  colors.text,
      backgroundColor: dark ? '#505050' : '#f5f5f5',
    },
    padding:{
      paddingLeft:20, 
      paddingRight: 20
    }
  });

  const groupData = (data) => {
    const months = ['January','February','March','April','May','June','July','August','September','October','November','December'];
    return data.reduce((acc, item) => {
      const date = new Date(item.time);
      const month = months[date.getMonth()]
      const year = date.getFullYear();
      const title = `${month} ${year}`;
      const monthData = acc.find((item) => item.title === title);
      if (monthData) {
        monthData.data.push(item);
      } else {
        acc.push({ title: title, data: [item] });
      }
    
      return acc;
    }, []);
  }

  const TransactionItem = ({ item, name, date, amount, time, last}) => {
    const amountColor = amount >= 0 ? 'green' : 'red';
    return (
      <View style={[stylesInternal.item,last ? {} : {borderBottomWidth: 1, borderBottomColor: 'lightgray'}]}>
        <View style={stylesInternal.leftContainer}>
          <ScrollView horizontal={true}>
            <Text style={stylesInternal.name}>{name}</Text>
          </ScrollView>
          <Text style={stylesInternal.date}>{date} at {time}</Text>
        </View>
        <View style={stylesInternal.rightContainer}>
          <Text style={[stylesInternal.amount, { color: amountColor }]}>{item.formatted_amount.string}</Text>
        </View>
      </View>
    );
  };

  if (isLoading){
    return <Loading/>
  }
  
  return (
    <View style={{flex:1,  margin: 4, marginBottom: 54}} >
              <View style={[stylesInternal.container]}>
                  <SectionList 
                    ListEmptyComponent={<View style={stylesInternal.padding}><Text style={styles(dark, colors).text}>{'\nYou have no bank accounts\n'}</Text></View>}
                    sections={groupData(bankData)} 
                    renderSectionHeader={({section: {title}}) => (<Text style={stylesInternal.header}>{title}</Text>)}
                    renderItem={({item, index, section}) =>{
                      return (
                        <View style={stylesInternal.padding}>
                        <TransactionItem
                          item={item}
                          name={item.info}
                          amount={item.amount}
                          date={displayDate(item.time)}
                          time={displayTime(item.time)}
                          last={index == section.data.length-1}/>
                        </View>)
                      }}
                      
                  />
              </View>
      </View>
  );
}


export default BankTransactionsScreen