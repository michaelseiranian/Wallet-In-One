import React, {createContext, useEffect, useContext, useState, AsyncStorage} from 'react';
import {lightColors, darkColors} from './colors';
import {useColorScheme} from 'react-native';
export const ThemeContext = createContext({
    dark: false,
    colors: lightColors,
    setScheme: () => {},
    update: () => {}
});

import * as SecureStore from 'expo-secure-store';

export const ThemeProvider = props => {
    const defaultColorScheme = useColorScheme(); // colorScheme is either 'dark', 'light' or 'null'
    const [isDark, setIsDark] = useState(false);

    async function loadDarkModeSettings(value = 'default') {
        // colorScheme is either 'dark', 'light' or 'null'
        var darkSetting;
        if (value === "default"){
            darkSetting = await SecureStore.getItemAsync('darkModeSettings');
        }
        else{
            darkSetting = value;
        }

        console.log('settings, default: ', darkSetting, defaultColorScheme,value)

        if (darkSetting === 'true') {
            setIsDark(true)
        }
        else if (darkSetting === 'false') {
            setIsDark(false)
        }
        else if (defaultColorScheme == 'dark') {
            setIsDark(true)
        }
        else if (defaultColorScheme == 'light') {
            setIsDark(false)
        }
        else {
            setIsDark(false)
        }
    }

    // Load Dark Mode Setting
    useEffect(() => {    
        loadDarkModeSettings();
    }, [defaultColorScheme]);

    const defaultTheme = {
        dark: isDark,
        colors: isDark ? darkColors : lightColors,
        setScheme: scheme => setIsDark(scheme === 'dark'),
        update: loadDarkModeSettings,
    };
    return (
        <ThemeContext.Provider value={defaultTheme}>
            {props.children}
        </ThemeContext.Provider>
    );
};

// creating a custom hook for accessing all the values

export const useTheme = () => useContext(ThemeContext);