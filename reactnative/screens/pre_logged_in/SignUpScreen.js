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
import { userContext } from "../../data";

import { api_url, login } from "../../authentication";
import * as SecureStore from "expo-secure-store";

export default function SignUpScreen({ navigation }) {

  const {dark, colors, setScheme} = useTheme();

  const [user, setUser] = useContext(userContext);

  const [username, setUsername] = useState();
  const [email, setEmail] = useState();
  const [firstName, setFirstName] = useState();
  const [lastName, setLastName] = useState();
  const [password, setPassword] = useState();
  const [passwordConfirmation, setPasswordConfirmation] = useState();

  const [errors, setErrors] = useState({});

  Notifications.setNotificationHandler({
    handleNotification: async () => {
      return {
        shouldShowAlert: true,
        shouldPlaySound: true,
        shouldSetBadge: true,
      };
    },
  });

  //192.168.1.81,10.0.2.2
  const signUpHandler = () => {
    fetch(api_url + "/sign_up/", {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        first_name: firstName,
        last_name: lastName,
        username: username,
        email: email,
        new_password: password,
        password_confirmation: passwordConfirmation,
      }),
    })
      .then((res) =>
        res.json().then((data) => ({ status: res.status, body: data }))
      )
      .then(async (data) => {
        // console.log('Response:', data);
        if (data["status"] == 400) {
          setErrors(data["body"]);
          Alert.alert("Error", "There were some errors");
        } else if (data["status"] == 201) {
          Alert.alert("Success", "Account created successfully");
          const notificationEnabled = await SecureStore.getItemAsync(
            "notificationSettings"
          );
          if (notificationEnabled == "true") {
            await Notifications.requestPermissionsAsync();
            await Notifications.scheduleNotificationAsync({
              content: {
                title: "You have successfully signed up!",
                body: "Manage the notifications from the settings",
              },
              trigger: null,
            });
          }
          else if (notificationEnabled == "false") {
            //set it to true
            await SecureStore.setItemAsync("notificationSettings", "true");
            await Notifications.requestPermissionsAsync();
            await Notifications.scheduleNotificationAsync({
              content: {
                title: "You have successfully signed up!",
                body: "Manage the notifications from the settings",
              },
              trigger: null,
            });
          }
          await login(username, password, user, setUser);
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  const inputStyle = (name) => {
    if (name in errors) {
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

      <Text style={[stylesInternal.text, styles(dark, colors).text]}>Username:</Text>
      <TextInput
        autoCapitalize='none'
        autoCorrect={false}
        style={[inputStyle("username"), styles(dark, colors).input, {color: colors?.text}]}
        onChangeText={setUsername}
        testID="username"
      />
      <ErrorMessage name="username"></ErrorMessage>

      <Text style={[stylesInternal.text, styles(dark, colors).text]}>Email:</Text>
      <TextInput
        autoCapitalize='none'
        autoCorrect={false}
        style={[inputStyle("email"), styles(dark, colors).input, {color: colors?.text}]}
        onChangeText={setEmail}
        testID="email"
      />
      <ErrorMessage name="email"></ErrorMessage>

      <Text style={[stylesInternal.text, styles(dark, colors).text]}>First Name:</Text>
      <TextInput
        autoCapitalize='none'
        autoCorrect={false}
        style={[inputStyle("first_name"), styles(dark, colors).input, {color: colors?.text}]}
        onChangeText={setFirstName}
        testID="first_name"
      />
      <ErrorMessage name="first_name"></ErrorMessage>

      <Text style={[stylesInternal.text, styles(dark, colors).text]}>Last Name:</Text>
      <TextInput
        autoCapitalize='none'
        autoCorrect={false}
        style={[inputStyle("last_name"), styles(dark, colors).input, {color: colors?.text}]}
        onChangeText={setLastName}
        testID="last_name"
      />
      <ErrorMessage name="last_name"></ErrorMessage>

      <Text style={[stylesInternal.text, styles(dark, colors).text]}>Password:</Text>
      <TextInput
        autoCapitalize='none'
        autoCorrect={false}
        style={[inputStyle("new_password"), styles(dark, colors).input, {color: colors?.text}]}
        onChangeText={setPassword}
        secureTextEntry={true}
        testID="new_password"
      />
      <ErrorMessage name="new_password"></ErrorMessage>

      <Text style={[stylesInternal.text, styles(dark, colors).text]}>Password Confirmation:</Text>
      <TextInput
        autoCapitalize='none'
        autoCorrect={false}
        style={[inputStyle("password_confirmation"), styles(dark, colors).input, {color: colors?.text}]}
        onChangeText={setPasswordConfirmation}
        secureTextEntry={true}
        testID="password_confirmation"
      />
      <ErrorMessage name="password_confirmation"></ErrorMessage>

      <View style={stylesInternal.parent}>
        <Button style={stylesInternal.button} title="Sign Up" onPress={signUpHandler} />
        {/* <Button style={stylesInternal.button} title="Login" onPress={() => setUser({...user, 'signedIn': true})} /> */}
      </View>
    </ScrollView>
  );
}

const stylesInternal = StyleSheet.create({
  container: {
    width: "100%",
    padding: 20,
  },
  parent: {
    marginTop: 20,
    marginBottom: 40,
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