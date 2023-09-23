import { useState } from 'react';
import {ThemeProvider} from './src/theme/ThemeProvider'

import 'react-native-gesture-handler';
import Navigation from './Navigation';


import { userContext } from './data';
import {StatusBar} from "expo-status-bar";

export default function App() {
  
  const user = useState({
    'signedIn': false
  });

  return (
    <ThemeProvider>
      <userContext.Provider value={user}>
        <StatusBar barStyle="dark-content" />
        <Navigation></Navigation>
      </userContext.Provider>
    </ThemeProvider>
  );
}
