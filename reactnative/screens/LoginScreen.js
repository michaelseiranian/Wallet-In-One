import { StatusBar } from "expo-status-bar";
import {
  StyleSheet,
  Text,
  View,
  ScrollView,
  Button,
  TextInput,
  Alert,
} from "react-native";
import * as Notifications from "expo-notifications";
import { useTheme } from 'reactnative/src/theme/ThemeProvider';
import {styles} from 'reactnative/screens/All_Styles.style.js';

import { useContext, useState } from "react";
import { userContext } from "../data";

import { login } from "../authentication";


import * as SecureStore from "expo-secure-store";

export default function SignUpScreen({ navigation }) {

  const {dark, colors, setScheme} = useTheme();

  const [user, setUser] = useContext(userContext);

  const [username, setUsername] = useState();
  const [password, setPassword] = useState();

  const [errors, setErrors] = useState({});

  const loginHandler = async () => {
    var response = await login(username, password, user, setUser);
    if (response.status == "Error") {
      Alert.alert("Error", response.body["message"]);
    } else if (response.status == 400 && response.body) {
      setErrors(response.body);

      if (response.body["non_field_errors"]) {
        Alert.alert("Error", "Login Error");
      }
    } else {
      console.log("Login Successful")
      await sendLogInNotification();
    }
  };
Notifications.setNotificationHandler({
    handleNotification: async () => {
      return {
        shouldShowAlert: true,
        shouldPlaySound: true,
        shouldSetBadge: true,
      };
    },
  });

const sendLogInNotification = async () => {
    const notificationEnabled = await SecureStore.getItemAsync(
      "notificationSettings"
    );
    console.log("notificationSettings value:", notificationEnabled)
    if (notificationEnabled === "true") {
      await Notifications.requestPermissionsAsync();
      await Notifications.scheduleNotificationAsync({
        content: {
          title: "You have successfully logged in!",
          body: "You can now access all the features of the app.",
        },
        trigger: null,
      });
    }

  };

  const inputStyle = (name) => {
    if (name in errors || "non_field_errors" in errors) {
      return [stylesInternal.input, stylesInternal.error];
    }
    return [stylesInternal.input];
  };

  function ErrorMessage(props) {
    if (props.name in errors) {
      return (
        <>
          {errors[props.name].map((value, index) => {
            return (
              <Text key={index} style={stylesInternal.errorText}>
                {value}
              </Text>
            );
          })}
        </>
      );
    }
    return null;
  }

  return (
    <ScrollView style={[stylesInternal.container, styles(dark, colors).container]}>
      <StatusBar style="auto" />

      <Text style={[stylesInternal.text, styles(dark, colors)?.text]}>Username:</Text>
      <TextInput
        autoCapitalize='none'
        autoCorrect={false}
        style={[inputStyle("username"), styles(dark, colors)?.input, {color: colors?.text}]}
        onChangeText={setUsername}
        testID="username"
      />
      <ErrorMessage name="username"></ErrorMessage>

      <Text style={[stylesInternal.text, styles(dark, colors)?.text]}>Password:</Text>
      <TextInput
        autoCapitalize='none'
        autoCorrect={false}
        style={[inputStyle("password"), styles(dark, colors)?.input, {color: colors?.text}]}
        onChangeText={setPassword}
        secureTextEntry={true}
        testID="password"
      />
      <ErrorMessage name="password"></ErrorMessage>
      <ErrorMessage name="non_field_errors"></ErrorMessage>

      <View style={stylesInternal.parent}>
        <Button style={stylesInternal.button} title="Log In" onPress={loginHandler} />
      </View>
    </ScrollView>
  );
}

const stylesInternal = StyleSheet.create({
  container: {
    width: "100%",
    padding: 30,
  },
  parent: {
    marginTop: 20,
    flex: 1,
    width: "100%",
    alignSelf: "flex-start",
  },
  text: {
    marginTop: 10,
    marginBottom: 10,
  },
  input: {
    height: 40,
    width: "100%",
    borderWidth: 0.5,
    padding: 10,
    borderColor: "gray",
    borderRadius: 5,
  },
  button: {},
  error: {
    borderColor: "red",
  },
  errorText: {
    marginLeft: 10,
    color: "red",
  },
});