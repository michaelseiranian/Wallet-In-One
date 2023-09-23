import { View, ActivityIndicator } from 'react-native';
import { useTheme } from 'reactnative/src/theme/ThemeProvider'

export default function Loading() {

  const {dark, colors, setScheme} = useTheme();

  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: colors.background }}>
        <ActivityIndicator color={colors.primary} size="large" />
    </View>
  );
}
