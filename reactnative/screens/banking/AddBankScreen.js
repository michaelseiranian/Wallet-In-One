import { StatusBar } from 'expo-status-bar';
import { useEffect, useState } from 'react'
import { StyleSheet, Text, View, ScrollView, Button, FlatList, TouchableOpacity, Image, TextInput,ActivityIndicator, Alert} from 'react-native';
import AuthWebView from './AuthView';
import { auth_get, auth_post} from '../../authentication'
import Loading from './Loading'
import { useTheme } from 'reactnative/src/theme/ThemeProvider'
import {styles} from 'reactnative/screens/All_Styles.style.js'

export default function AddBankScreen({ navigation }) {
    const [ search, setSearch ] = useState('') // Stores contents of search box
    const [ data, setData ] = useState([])     // Stores all bank data
    const [ bankData, setbankData ] = useState([])        // Stores filtered bankdata
    const [ isLoading, setIsLoading ] = useState(true)    // Initial load

    const [ bankAuthURL, setbankAuthURL ] = useState(null)// Link to authenticate with selected bank
    const [ authComplete, setAuthComplete ] = useState(false)
    const [ savedBanks, setSavedBanks ] = useState(null)

    const {dark, colors, setScheme} = useTheme();

    const reset = () => {
        setbankAuthURL(null)
        setAuthComplete(false)
        setSavedBanks(null)
    }

    const stylesInternal = StyleSheet.create({
        bankingContainer: {
            width: '100%',
            paddingLeft: 20,
            paddingRight: 20,
            paddingBottom: 0,
            borderWidth: 1,
            borderRadius: 5,
            borderColor: dark ? colors.background : '#ddd',
            overflow: 'hidden',
            backgroundColor: colors.background
          },
          bankingItem:{
            flexDirection: 'row',
            alignItems: 'center',
            padding: 10
          },
          bankingImage:{
              width: 50, 
              height: 50,
              marginRight: 10,
              resizeMode: 'contain',
          },
          bankingInput:{
            height: 40,
            width: '100%',
            borderWidth: 0.5,
            padding: 10,
            borderColor: 'gray',
            borderRadius: 5,
            marginTop: 5,
            marginBottom: 5,
            color: colors.text,
            backgroundColor: colors.background
          },
      });
    
    
    useEffect(() =>{
        const fetchData = async () => {
            console.log('fetching')
            const response = await auth_get('/banking/bank_list/')
            if (response.status == 200){
                setData(response.body)
                setbankData(response.body)
                setIsLoading(false)
            }
        }
        fetchData()
    }, [])
    
    const selectItem = (item) => {

        const getAuthURL = async (id) => {
            console.log('fetching url')
            const response = await auth_get(`/banking/auth_page/${id}/`)
            if (response.status == 200){
                setbankAuthURL(response.body.url)
            }
            else{
                console.log('error', response)
            }
        }
        console.log(item.id)
        getAuthURL(item.id)
    }

    const updateSearch = (string) => {
        setSearch(string)
        const searchString = string.toLowerCase()
        setbankData(data.filter(item => item.name.toLowerCase().includes(searchString)))
    }

    const detectFinish = (event) => {
        if (!authComplete && event.url.includes('example.com')) {
            setAuthComplete(true)
            updateServer(bankAuthURL)
            setbankAuthURL(null)
        }
    }

    const updateServer = (url) => {
        const sendLink = async () => {
            const response = await auth_post('/banking/finish_auth/',{'url': url})
            console.log(response)
            if (response.status == 200){
                setSavedBanks(response.body)
            }
            else if (response.status == 400 && response.body.error){
                Alert.alert("Error", response.body.error)
                reset()
            }
            else{
                Alert.alert("Error", "There was an error with the server, try again")
                reset()
            }
        }
        sendLink()
    }

    if (isLoading){
        return <Loading/>
    }

    if (bankAuthURL){
        return <AuthWebView url={bankAuthURL} onCancel={()=>{setbankAuthURL(null)}} stateChange={detectFinish} />
    }

    if (authComplete){
        return (
            <View
                style={styles(dark, colors).container}
            >
                {!savedBanks ? (
                    <TouchableOpacity style={{flex: 1,justifyContent:'center', alignItems:'center'}} onPress={()=>setAuthComplete(false)}>
                        <Text style={styles(dark, colors).text}>Bank Authentication Finished</Text>
                        <Text style={styles(dark, colors).text}>Waiting For server</Text>
                        <ActivityIndicator/>
                    </TouchableOpacity>
                ):(
                    <>
                        <View style={{flex: 1,justifyContent:'center', alignItems:'center'}}>
                            <Text style={styles(dark, colors).text}> Bank account(s) have been added</Text>
                        </View>
                        <Button title="Back" onPress={reset}/>
                    </>
                )}
            </View>
        )
    }
    
    return (
        <View
            style={[{flex:1, margin: 4, marginBottom: 54}]}
        >
                <TextInput
                    autoCapitalize='none'
                    autoCorrect={false}
                    style={stylesInternal.bankingInput}
                    placeholder='Search'
                    placeholderTextColor= {colors.text}
                    value={search}
                    onChangeText={updateSearch}
                />
                <View style={stylesInternal.bankingContainer}>
                    <FlatList data={bankData} renderItem={({item, index}) =>{
                        return (
                            <TouchableOpacity onPress={()=>selectItem(item)} style={stylesInternal.bankingItem}>
                                <Image                                   
                                    source={{ uri: item.logo }}
                                    style={stylesInternal.bankingImage}
                                />
                                <Text style={styles(dark, colors).text} key={index}>{item.name}</Text>
                            </TouchableOpacity>)
                        }}
                        ListEmptyComponent={<Text style={styles(dark, colors).text}>{'\nNo banks found\n'}</Text>}
                    />
                </View>
        </View>
    );
}
