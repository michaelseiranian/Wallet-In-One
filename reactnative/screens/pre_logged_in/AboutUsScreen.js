import {
    StyleSheet,
    Text,
    TouchableOpacity,
    View,
    Image,
    ScrollView,
    ImageBackground,
  } from "react-native";
import React from "react";
import { useTheme } from 'reactnative/src/theme/ThemeProvider';
import {styles} from 'reactnative/screens/All_Styles.style.js';
  
export default function AboutUsScreen ({ navigation }) {

    const {dark, colors, setScheme} = useTheme();

    const stylesInternal = StyleSheet.create({
      aboutContainer: {
        display: "flex",
        flex: 1
      },
      background: {
          width: '100%',
          height: '100%'
      },
      logo:{
          width: 290,
          height: 280,
          marginTop: '-10%',
          alignSelf:'center'
      },
      imgStyle: {
        width: 370,
        height: 150,
        borderRadius: 40,
        marginTop: '-10%',
        alignSelf:'center'
      },
      paraStyle: {
        fontSize: 16,
        paddingBottom: 30,
      },
      aboutLayout: {
        backgroundColor: colors.primary,
        paddingHorizontal: 30,
        marginVertical: 30,
        paddingBottom: 10
      },
      aboutSubHeader: {
        fontSize: 18,
        color: "#fff",
        textTransform: "uppercase",
        fontWeight: "500",
        marginVertical: 15,
        alignSelf: "center",
      },
      aboutPara: {
        color: "#fff",
      },
      homepage: {
        backgroundColor: 'white',
        color: colors.primary,
        width: "75%",
        borderRadius: 25,
        textAlign: 'center',
        fontWeight: 'bold',
        marginLeft: '11%',
        padding: "2%",
        fontSize:  27,
        marginTop: '-2%'
      },
      developers: {
        backgroundColor: 'black',
        color: colors.primary,
        width: "40%",
        borderRadius: 25,
        textAlign: 'center',
        fontWeight: 'bold',
        padding: "2%",
        fontSize:  17,
        marginTop: '-4%',
        alignSelf: 'center',
      },
    });

    return (
      <ImageBackground
        source={require('reactnative/assets/background.jpg')}
        style={stylesInternal.background}
      >
      <ScrollView
      contentContainerStyle={{
        flexGrow : 1,
        justifyContent : 'center',
        paddingBottom: 20
        }}
      style={stylesInternal.aboutContainer}
      >
        <Image
            source={require('reactnative/assets/logo.png')}
            style={stylesInternal.logo}
            resizeMode="contain"
          >
        </Image>
        <View>
          <Image
            style={stylesInternal.imgStyle}
            source={require('reactnative/assets/wallets.webp')}
          />
        </View>
  
        <View
        contentContainerStyle={{
            paddingBottom: 30,
            }}
        style={stylesInternal.aboutLayout}
        
        >
          <Text style={stylesInternal.aboutSubHeader}> About us </Text>
          <Text style={[stylesInternal.paraStyle, stylesInternal.aboutPara]}>
            Welcome to Wallet-In-One! We are an all in one central finance
            app where you can access your credit cards, debit cards, stocks and
            crytocurrency. Simply connect your respective accounts and view
            the latest changes in your finances. {"\n"}
            This app was developed by second year students from King's College 
            London on the Computer Science course for the module 'Software
            Engineering Group Project' for a client. All IP belongs to the client
            and further development is to be continued by said client.
          </Text>
          <TouchableOpacity
            onPress={() => navigation.navigate('Developer Info')}
          >
             <Text style={stylesInternal.developers}>Meet the team!</Text>
          </TouchableOpacity>
        </View>
        
        <TouchableOpacity
            onPress={() => navigation.navigate('Start')}
        >
           <Text style={stylesInternal.homepage}>Home Page</Text>
        </TouchableOpacity>
  
      </ScrollView>
      </ImageBackground>
    );
  };