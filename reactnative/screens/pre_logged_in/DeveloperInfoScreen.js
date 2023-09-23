import {
    Linking,
    StyleSheet,
    Text,
    TouchableOpacity,
    View,
    Image,
    ScrollView,
    ImageBackground,
    div,
  } from "react-native";
import React from "react";
import { useTheme } from 'reactnative/src/theme/ThemeProvider';

export default function DeveloperInfoScreen ({ navigation }) {

    const {dark, colors, setScheme} = useTheme();

    const styles = StyleSheet.create({
        aboutUs: {
            backgroundColor: colors.primary,
            color: 'black',
            width: "60%",
            borderRadius: 25,
            textAlign: 'center',
            fontWeight: 'bold',
            padding: "2%",
            fontSize:  20,
            alignSelf: 'center',
        },
        developerName: {
            fontSize: 18,
            color: "#fff",
            textTransform: "uppercase",
            fontWeight: "500",
            marginLeft: '-57%',
            alignSelf: "center",
        },
        developerPage: {
            marginTop: 20,
        },
        background: {
            width: '100%',
            height: '100%'
        },
        iconStyle: {
            width: "100%",
            height: 50,
            aspectRatio: 1,
        },
        buttonStyle: {
            borderRadius: 5,
            paddingVertical: -10,
            paddingHorizontal: 28,
            marginRight: '60%',
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            marginVertical: 15,
        },
        meetTheTeam: {
            fontSize: 18,
            color: "#fff",
            textTransform: "uppercase",
            fontWeight: "500",
            marginVertical: 15,
            alignSelf: "center",
        },
        developersPara: {
            color: "#fff",
        },
        paraStyle: {
            fontSize: 16,
            color: colors.primary,
            paddingBottom: 25,
        },
        textBoxLayout: {
            backgroundColor: colors.primary,
            paddingHorizontal: 30,
            marginVertical: 30,
        },
        logo:{
            width: 290,
            height: 280,
            marginTop: '-10%',
            marginBottom: '-15%',
            alignSelf:'center'
        },
    })

    return (
        <ImageBackground
            source={require('reactnative/assets/background.jpg')}
            style={styles.background}
        >
        <ScrollView
        contentContainerStyle={{
            flexGrow : 1,
            justifyContent : 'center',
            paddingBottom: 15
            }}
        style={styles.developerPage}
        >

        <Image
            source={require('reactnative/assets/logo.png')}
            style={styles.logo}
            resizeMode="contain"
        >
        </Image>

        <View
        contentContainerStyle={{
            paddingBottom: 30,
            }}
        style={styles.textBoxLayout}
        >

        <Text style={styles.meetTheTeam}> Meet the team </Text>
        <Text style={[styles.paraStyle, styles.developersPara]}>
            This app was developed by second year students from King's College 
            London on the Computer Science course for the module 'Software
            Engineering Group Project'. {"\n"}
            Our team totals 8 students, feel free to visit our Github accounts
            and view our other projects by tapping on the icons below.
        </Text>
        </View>

            <View style={{ flexDirection:"row"}}>    
                <TouchableOpacity
                style={styles.buttonStyle}
                onPress={() =>
                    Linking.openURL(
                    "https://github.com/AbbasBinVakas"
                    )
                }
                testID={'GithubButtonTestAbbas'}>
                <Image
                style={styles.iconStyle}
                source={require('reactnative/assets/github.png')}
                />
                </TouchableOpacity>
                <Text style={styles.developerName}> Abbas Bin Vakas </Text>
            </View>
            <View style={{ flexDirection:"row"}}>    
                <TouchableOpacity
                style={styles.buttonStyle}
                onPress={() =>
                    Linking.openURL(
                    "https://github.com/YusufKCL"
                    )
                }
                testID={'GithubButtonTestYusuf'}>
                <Image
                style={styles.iconStyle}
                source={require('reactnative/assets/github.png')}
                />
                </TouchableOpacity>
                <Text style={styles.developerName}> Yusuf Abdulrahman </Text>
            </View>
            <View style={{ flexDirection:"row"}}>    
                <TouchableOpacity
                style={styles.buttonStyle}
                onPress={() =>
                    Linking.openURL(
                    "https://github.com/XEZ1"
                    )
                }
                testID={'GithubButtonTestEzat'}>
                <Image
                style={styles.iconStyle}
                source={require('reactnative/assets/github.png')}
                />
                </TouchableOpacity>
                <Text style={styles.developerName}> Ezzat Alsalibi </Text>
            </View>
            <View style={{ flexDirection:"row"}}>    
                <TouchableOpacity
                style={styles.buttonStyle}
                onPress={() =>
                    Linking.openURL(
                    "https://github.com/Shozab-N18"
                    )
                }
                testID={'GithubButtonTestShozab'}>
                <Image
                style={styles.iconStyle}
                source={require('reactnative/assets/github.png')}
                />
                </TouchableOpacity>
                <Text style={styles.developerName}> Shozab Anwar Siddique </Text>
            </View>
            <View style={{ flexDirection:"row"}}>    
                <TouchableOpacity
                style={styles.buttonStyle}
                onPress={() =>
                    Linking.openURL(
                    "https://github.com/JamalBoustani"
                    )
                }
                testID={'GithubButtonTestJamal'}>
                <Image
                style={styles.iconStyle}
                source={require('reactnative/assets/github.png')}
                />
                </TouchableOpacity>
                <Text style={styles.developerName}> Jamal Boustani </Text>
            </View>
            <View style={{ flexDirection:"row"}}>    
                <TouchableOpacity
                style={styles.buttonStyle}
                onPress={() =>
                    Linking.openURL(
                    "https://github.com/krishnapk7"
                    )
                }
                testID={'GithubButtonTestKrishna'}>
                <Image
                style={styles.iconStyle}
                source={require('reactnative/assets/github.png')}
                />
                </TouchableOpacity>
                <Text style={styles.developerName}> Krishna Prasanna Kumar </Text>
            </View>
            <View style={{ flexDirection:"row"}}>    
                <TouchableOpacity
                style={styles.buttonStyle}
                onPress={() =>
                    Linking.openURL(
                    "https://github.com/mohawk49"
                    )
                }
                testID={'GithubButtonTestMichael'}>
                <Image
                style={styles.iconStyle}
                source={require('reactnative/assets/github.png')}
                />
                </TouchableOpacity>
                <Text style={styles.developerName}> Michael Seiranian </Text>
            </View>
            <View style={{ flexDirection:"row"}}>    
                <TouchableOpacity
                style={styles.buttonStyle}
                onPress={() =>
                    Linking.openURL(
                    "https://github.com/mrmatyog"
                    )
                }
                testID={'GithubButtonTestMatushan'}>
                <Image
                style={styles.iconStyle}
                source={require('reactnative/assets/github.png')}
                />
                </TouchableOpacity>
                <Text style={styles.developerName}> Matushan Yogaraj </Text>
            </View>

            <TouchableOpacity
                onPress={() => navigation.navigate('About Us')}
            >
            <Text style={styles.aboutUs}>Back to About Us</Text>
            </TouchableOpacity>  
        </ScrollView>   
        </ImageBackground>
    )
}