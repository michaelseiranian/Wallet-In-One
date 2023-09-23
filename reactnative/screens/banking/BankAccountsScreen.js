import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View, ScrollView, Button, TextInput, Alert, FlatList , TouchableOpacity, Image} from 'react-native';
import { useState, useEffect } from 'react';
import { auth_get} from '../../authentication'
import { useIsFocused } from '@react-navigation/native';
import Loading from './Loading'
import { useTheme } from 'reactnative/src/theme/ThemeProvider'
import {styles} from 'reactnative/screens/All_Styles.style.js'
import AntDesign from 'react-native-vector-icons/AntDesign';
import FontAwesome from 'react-native-vector-icons/FontAwesome';
import ConditionalModal from '../Modal';

export default function BankAccountsScreen({ navigation }) {
  const [ isLoading, setIsLoading ] = useState(true)
  const [ bankData, setBankData ] = useState([])
  const isFocused = useIsFocused();
  const {dark, colors, setScheme} = useTheme();
  const [modalVisible, setModalVisible] = useState(false);

  const deleteAccount = async (id) => {
    console.log(`delete_account /banking/delete_account/${id}/`)
    setIsLoading(true)
    await auth_get(`/banking/delete_account/${id}/`)
    fetchData();
  }

  const fetchData = async () => {
    console.log('fetch bank accounts data')
    setIsLoading(true)
    const response = await auth_get('/banking/user_accounts/')
    console.log('status', response.status)
    if (response.status == 200){
        setIsLoading(false)
        setBankData(response.body)
    }
  }

  useEffect(() =>{
    if(isFocused != false){fetchData()}
  }, [isFocused])

  const stylesInternal = StyleSheet.create({
    container: {
      width: '100%',
      paddingLeft: 20,
      paddingRight: 20,
      paddingBottom: 0,
      paddingTop: 10,
      borderRadius: 5,
      borderColor: dark ? colors.background : '#ddd',
      overflow: 'hidden',
    },
    row:{
      flexDirection: 'row',
      alignItems: 'flex-start',
    },
    item:{
      padding: 20,
      borderRadius: 10,
      marginBottom: 10,
    },
    item_error:{
      borderColor: 'red',
      borderWidth: 4,
    },
    name:{
      color: "white",
      fontWeight: 'bold',
      fontSize: 21,
    },
    amount:{
      color: "white",
      fontSize: 18,
    },
    iban:{
      color: 'rgba(255,255,255,0.5)',
      fontSize: 10,
      marginBottom: 3,
    },
    closeButton: {
      position: 'absolute',
      top: 10,
      right: 10,
      backgroundColor: 'red',
      width: 27,
      height: 27,
      borderRadius: 15,
      alignItems: 'center',
      justifyContent: 'center',
    },
    closeButton2: {
      position: 'absolute',
      bottom: 20,
      right: 10,
      backgroundColor: '#ecba1d',
      borderRadius: 15,
      width: 27,
      height: 27,
      alignItems: 'center',
      justifyContent: 'center',
    },
    closeButtonText: {
      color: 'white',
      fontSize: 20,
      fontWeight: 'bold',
    },
    button: {
      padding: 10,
      borderRadius: 10,
      marginVertical: 4,
      marginHorizontal: 8,
      backgroundColor: colors.primary,
      alignSelf: 'center',
    },
    buttonText: {
      textAlign: 'center',
      fontWeight: 'bold',
      color: colors.text,
    },
  });
  
  

  if (isLoading){
    return <Loading/>
}

  return (
    <View style={{flex:1, backgroundColor: colors.background}} >

        <View style={{flexDirection:'row', justifyContent: 'center'}}>
          <TouchableOpacity
            style={stylesInternal.button}
            onPress={() => navigation.navigate('Bank Insights')}
          >
            <Text style={stylesInternal.buttonText}>Bank Insights</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={stylesInternal.button}
            onPress={() => navigation.navigate("All Bank Transactions")}
          >
            <Text style={stylesInternal.buttonText}>All Transactions</Text>
          </TouchableOpacity>
        </View>

              <View style={[stylesInternal.container]}>
                  <FlatList data={bankData} renderItem={({item, index}) =>{
                      return ( 
                        BankAccount(item, index)) 
                      }}
                      ListEmptyComponent={<Text style={styles(dark, colors).text}>{'\nYou have no bank accounts\n'}</Text>}
                  />
              </View>
      </View>
  );

  function BankAccount(item, index) {
    var mainStyle = [stylesInternal.item, { backgroundColor: item.color }]
    if (item.disabled){
      mainStyle.push(stylesInternal.item_error)
    }

    return (
      <>
      <TouchableOpacity testID="account" style={mainStyle} key={index} onPress={ () => {  navigation.navigate('Bank Transactions', { accountID: item.id })}}>
        <View style={stylesInternal.row}>
          <Image
            source={{ uri: item.institution_logo }}
            style={{ width: 70, height: 70, marginRight: 10, resizeMode: 'contain', borderRadius: 10, backgroundColor: 'white' }} />
          <View style={{ borderRadius: 10 }}>
            <Text style={stylesInternal.name}>{item.institution_name}</Text>
            <Text style={stylesInternal.iban}>{item.iban}</Text>
            <Text style={stylesInternal.amount}>{item.balance.string}</Text>
          </View>
        </View>
      </TouchableOpacity>
      <TouchableOpacity testID="close1" style={stylesInternal.closeButton} onPress={() => setModalVisible(true)}>
        <FontAwesome style={stylesInternal.closeButtonText} name="close" size= {20}/>
      </TouchableOpacity>

      <ConditionalModal
        headerText={"Remove Your Bank Account"}
        bodyText={"Are you sure you want to remove your bank account?"}
        visible={modalVisible}
        onEvent={() => deleteAccount(item.id)}
        onClose={() => setModalVisible(false)}
      />

      {item.disabled?(
      <TouchableOpacity testID="close2" style={stylesInternal.closeButton2} onPress={() => Alert.alert('Warning','This account is not connected anymore. Please delete and readd this account.') }>
        <FontAwesome style={stylesInternal.closeButtonText} name="exclamation" size= {20}/>
      </TouchableOpacity>):(<></>)}
      
    </>

)
  }
}