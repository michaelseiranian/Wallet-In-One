import React, { useState } from 'react';
import { StyleSheet, Pressable, View, Text, TextInput, Button, Alert } from 'react-native';
import * as SecureStore from "expo-secure-store";
import { useTheme } from 'reactnative/src/theme/ThemeProvider';
import { api_url } from '../../authentication';


export default function ExchangeCredentials({ route, navigation }) {
  const [apiKey, setApiKey] = useState('');
  const [secretKey, setSecretKey] = useState('');
  const {dark, colors, setScheme} = useTheme();
  const {exchange} = route.params;

  // The following function is triggered on press of Submit button
  const handleSubmit = async () => {
    // If fields are empty, display appropriate error message
    if (!apiKey || !secretKey) {
      Alert.alert('Error', 'Please enter both API Key and Secret Key.');
      return;
    }
    // else, try to find the exchange account and Post into backend
    try {
      const response = await fetch(`${api_url}/crypto-exchanges/${exchange.toLowerCase()}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Token ${await SecureStore.getItemAsync("token")}`,
        },
        body: JSON.stringify({ api_key: apiKey, secret_key: secretKey }),
      });
      const data = await response.json();
      const statusCode = response.status;
      // Success
      if (statusCode === 200) {
        navigation.navigate('Crypto Wallets & Exchanges');
      }
      // Error posting
      else {
        Alert.alert('Error', data["error"]);
      }
      // Any other error thrown in the try block
    } catch (error) {
      Alert.alert('Error', `An error occurred while retrieving ${exchange} account data.`);
    }
  };

  const styles = StyleSheet.create({
    titleContainer: {
      flexDirection: 'row',
      alignItems: 'center',
      marginBottom: 20,
    },
    title: {
      fontSize: 25,
      color: colors.text,
    },
    input:{
      height: 40,
      width: '100%',
      borderWidth: 0.5,
      padding: 10,
      borderColor: 'gray',
      borderRadius: 5,
      marginTop: 5,
      marginBottom: 10,
      color: colors.text,
      backgroundColor: colors.background

    },
  });

  return (
    <View style={{ padding: 20, backgroundColor:colors.background, flex: 1 }}>
      <View style={{ flexDirection: "row", alignItems: "center", marginBottom: 20 }}>
        <Text style={styles.title}>{exchange} Credentials:</Text>
      </View>
      {/*API key title and field*/}
      <Text style={{ fontSize: 20, marginBottom: 10, color: colors.text }}>API Key:</Text>
      <TextInput
        autoCapitalize='none'
        autoCorrect={false}
        value={apiKey}
        onChangeText={setApiKey}
        style={styles.input}
        testID="apiKeyInput"
      />
      {/*Secret key title and field*/}
      <Text style={{ fontSize: 20, marginBottom: 10, color: colors.text }}>Secret Key:</Text>
      <TextInput
        autoCapitalize='none'
        autoCorrect={false}
        value={secretKey}
        onChangeText={setSecretKey}
        secureTextEntry
        style={styles.input}
        testID="secretKeyInput"
      />
      {/*Submit button*/}
      <Button
        title="Submit"
        onPress={handleSubmit}
        color= {colors.primary}
        backgroundColor='#FFFF00'
        buttonStyle={{ borderRadius: 20 }}
      />
    </View>
  );
}
