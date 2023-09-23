import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  Switch,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  TouchableHighlight
} from 'react-native';
import * as Notifications from "expo-notifications";
import * as SecureStore from 'expo-secure-store';
import { logout } from '../authentication';
import { useContext } from 'react';
import { userContext } from '../data';
import { useTheme } from 'reactnative/src/theme/ThemeProvider'
import {styles} from 'reactnative/screens/All_Styles.style.js'
import Icon from 'react-native-vector-icons/Feather';

export default function SettingsPage ({ navigation }) {

  const [notifications, setNotifications] = useState(true);
  const [user, setUser] = useContext(userContext)
  const {dark, colors, setScheme, update} = useTheme();

  const stylesInternal = StyleSheet.create({
    container: {
      flex: 1,
    },
    title: {
      fontSize: 24,
      fontWeight: 'bold',
      marginBottom: 20
    },
    switchContainer: {
      flexDirection: 'row',
      alignItems: 'center',
      justifyContent: 'space-between',
      width: '80%'
    },
    logoutButton: {
      marginTop: 20
    },
    aboutUs: {
      backgroundColor: 'red',
      color: 'black',
      width: "30%",
      borderRadius: 25,
      textAlign: 'center',
      fontWeight: 'bold',
      padding: "2%",
      fontSize:  17,
      marginTop: '10%',
      alignSelf: 'center'
    },
    developers: {
      backgroundColor: 'black',
      color: 'red',
      width: "40%",
      borderRadius: 25,
      textAlign: 'center',
      fontWeight: 'bold',
      padding: "2%",
      fontSize:  17,
      marginTop: '10%',
      alignSelf: 'center',
    },
    button: {
      width: "75%",
      borderRadius: 25,
      textAlign: 'center',
      fontWeight: 'bold',
      marginTop: '4%',
      paddingHorizontal: "12%",
      paddingVertical: "2%",
      fontSize:  20,
    },
    item: {
      padding: 10,
      flexDirection: 'row',
      alignItems: 'center',
      justifyContent: 'space-between',
      borderBottomColor: '#ddd',
      borderBottomWidth: 1,
      height: 50
    },
    last_item: {
      borderBottomWidth: 0,
    },
  });

  const [selectedValue, setSelectedValue] = useState(null);

  function Item({label, value, style = stylesInternal.item}) {
    return <TouchableHighlight onPress={() => changeTheme(value)} underlayColor={dark?'#666':'#ddd'}>
      <View style={style}>
        <Text style={{color: colors?.text}}>{label}</Text>
        {selectedValue === value && (<Icon name={'check'} size={24} color={'green'} />)}
      </View>
    </TouchableHighlight>;
  }

  // Load notification setting
  useEffect(() => {
      async function loadNotificationSetting() {
    const initialValue = await SecureStore.getItemAsync('notificationSettings');
    if (initialValue === null) {
      await SecureStore.setItemAsync('notificationSettings', 'false');
      setNotifications(false);
    } else {
      setNotifications(initialValue === 'true');
    }
  }
  loadNotificationSetting();
}, []);

  Notifications.setNotificationHandler({
    handleNotification: async () => {
      return {
        shouldShowAlert: true,
        shouldPlaySound: true,
        shouldSetBadge: true,
      };
    },
  });



  // Toggle and save notification setting
  const toggleNotifications = async () => {

     setNotifications((previousState) => !previousState);
      const notificationSettings = (!notifications).toString();
      await SecureStore.setItemAsync("notificationSettings", notificationSettings);
    if (notificationSettings === "true") {
      Notifications.requestPermissionsAsync();
      Notifications.scheduleNotificationAsync({ content: {
          title: "Notifications enabled!",
        },
        trigger: null, });

    }
  };

  // Toggle and save theme setting
  const changeTheme = async (theme) => {
      setSelectedValue(theme)
      update(theme)
      if (theme){
        await SecureStore.setItemAsync('darkModeSettings', theme);
      }
      else{
        await SecureStore.deleteItemAsync('darkModeSettings');
      }
      const notificationSettings = notifications.toString();
      if (notificationSettings === "true") {
        Notifications.requestPermissionsAsync();
        Notifications.scheduleNotificationAsync({
          content: {
            title: "Theme changed successfully!",
          },
          trigger: null,
        });
      }
  };

  
  return (
    
    <ScrollView
      contentContainerStyle={{
        flexGrow : 1,
        justifyContent: 'center',
        alignItems: 'center',
        paddingBottom: 20,
        }}
      style={styles(dark, colors).container}
    >
      {/* Notifications section and toggle for enabling and disabling notifications */}
      <Text style={[styles(dark, colors).textBold, {fontSize: 24, marginBottom: 20}]}>Notifications</Text>
      <View style={stylesInternal.switchContainer}>
        <Text style={styles(dark, colors).text}>Receive notifications</Text>
        <Switch
          trackColor={{ false: "#767577", true: "#81b0ff" }}
          thumbColor={notifications ? "purple" : "#f4f3f4"}
          onValueChange={toggleNotifications}
          value={notifications}
        />
      </View>

      {/* Dark mode section and list for choosing between the 'System default' theme, light theme or dark theme*/}
      <Text style={[styles(dark, colors).textBold, {fontSize: 24, marginBottom: 20}]}>Themes</Text>
      <View style={[styles(dark, colors).list]}>
        <Item label={'System Default'} value={null} />
        <Item label={'Light Mode'} value={'false'}/>
        <Item label={'Dark Mode'} value={'true'} style={[stylesInternal.item, stylesInternal.last_item]}/>
      </View>

      {/* Button for logging out of the app */}
      <TouchableOpacity
        onPress={()=>{logout(user, setUser)}}
      >
        <Text style={[{backgroundColor: colors?.primary}, {color: "white"}, stylesInternal.button]}>Logout</Text>
      </TouchableOpacity>

    </ScrollView>
  );
}