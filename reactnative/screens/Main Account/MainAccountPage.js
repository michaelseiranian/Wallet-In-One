import { StatusBar } from 'expo-status-bar';
import {StyleSheet, Text, View, TouchableOpacity} from 'react-native';
import { useTheme } from 'reactnative/src/theme/ThemeProvider';
import { styles } from 'reactnative/screens/All_Styles.style.js';
import Icon from 'react-native-vector-icons/FontAwesome';
import Icon2 from 'react-native-vector-icons/Ionicons';

import React from 'react';


export default function MainAccountPage({ navigation }) {
    const { dark, colors, setScheme } = useTheme();

    const stylesInternal = StyleSheet.create({
        row: {
            flex: 1,
            flexDirection: 'row',
        },
        box: {
            flex: 1,
            borderRadius: 15,
            margin: 5,
            flexDirection: 'column',
            justifyContent: 'space-evenly',
            alignItems: 'center'
        },
        text: { 
            color: 'white', 
            fontSize: 23, 
            fontWeight: 'bold', 
            textAlign: 'center'
        }
    });

    return (
        <View style={[styles(dark, colors).container, {flexDirection: 'column', padding: 5,}]}>
            <TouchableOpacity
                style={[stylesInternal.box, { backgroundColor: '#5686f2' }]}
                onPress={() => navigation.navigate("Bank Accounts")}
            >
                <Icon style={{ color: 'white' }} name="bank" size={80} />
                <Text style={stylesInternal.text}>{'Bank Accounts'}</Text>
            </TouchableOpacity>
            <TouchableOpacity
                style={[stylesInternal.box, { backgroundColor: 'red' }]}
                onPress={() => navigation.navigate("Crypto Wallets & Exchanges")}
            >
                <Icon2 style={{ color: 'white' }} name="wallet" size={80} />
                <Text style={stylesInternal.text}>{'Cryptocurrency'}</Text>
            </TouchableOpacity>
            <TouchableOpacity
                style={[stylesInternal.box, { backgroundColor: '#55a755' }]}
                onPress={() => navigation.navigate("Stock Account List")}
            >
                <Icon style={{ color: 'white' }} name="line-chart" size={80} />
                <Text style={stylesInternal.text}>{'Stock Accounts'}</Text>
            </TouchableOpacity>
        </View>
    );
}
