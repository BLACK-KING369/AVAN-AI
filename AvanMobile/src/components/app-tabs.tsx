import { DarkTheme, ThemeProvider } from "expo-router";
import { useColorScheme } from "react-native";

export default function RootLayout() {
  const colorScheme = useColorScheme();

  return (
    <ThemeProvider value={DarkTheme}>
      <>
        {/* Expo Router automatically loads src/app/index.tsx */}
      </>
    </ThemeProvider>
  );
}