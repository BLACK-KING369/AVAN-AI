import React from "react";
import { View, Text, StyleSheet } from "react-native";

export default function HomeScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>◉ AVAN</Text>
      <Text style={styles.subtitle}>REMOTE COMMAND SYSTEM</Text>

      <View style={styles.status}>
        <Text style={styles.statusText}>● PC ONLINE</Text>
      </View>

      <Text style={styles.ready}>SYSTEM READY, BOSS</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#050909",
    alignItems: "center",
    justifyContent: "center",
  },

  title: {
    color: "#00ffcc",
    fontSize: 38,
    fontWeight: "900",
    letterSpacing: 5,
  },

  subtitle: {
    color: "#668888",
    fontSize: 11,
    letterSpacing: 3,
    marginTop: 8,
  },

  status: {
    marginTop: 35,
    borderWidth: 1,
    borderColor: "#00ff99",
    borderRadius: 8,
    paddingHorizontal: 20,
    paddingVertical: 10,
  },

  statusText: {
    color: "#00ff99",
    fontWeight: "700",
  },

  ready: {
    color: "#668888",
    marginTop: 25,
    fontFamily: "monospace",
  },
});