import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  Pressable,
  StyleSheet,
  StatusBar,
  ScrollView,
} from 'react-native';

export default function HomeScreen() {
  const [command, setCommand] = useState('');
  const [logs, setLogs] = useState<string[]>([
    '> Awaiting command...',
    '> Remote system ready.',
  ]);
  const [sending, setSending] = useState(false);

  const sendCommand = async () => {
    const trimmedCommand = command.trim();

    if (!trimmedCommand || sending) {
      return;
    }

    setSending(true);

    // Mobile console me command dikhao
    setLogs((prev) => [
      ...prev,
      `> ${trimmedCommand}`,
      '> Sending to PC...',
    ]);

    try {
      const response = await fetch(
       'http://10.64.232.160:8765/command' ,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            command: trimmedCommand,
          }),
        }
      );

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const data = await response.json();

      console.log('AVAN RESPONSE:', data);

      setLogs((prev) => [
        ...prev,
        `> PC: ${data.message || data.response || 'Command executed.'}`,
      ]);

      setCommand('');
    } catch (error) {
      console.log('CONNECTION ERROR:', error);

      setLogs((prev) => [
        ...prev,
        '> ERROR: PC connection failed.',
        '> Check Avan Remote Server and Wi-Fi.',
      ]);
    } finally {
      setSending(false);
    }
  };

  return (
    <View style={styles.container}>
      <StatusBar barStyle="light-content" />

      {/* HEADER */}
      <View style={styles.header}>
        <Text style={styles.logo}>◉ AVAN</Text>

        <Text style={styles.subtitle}>
          PERSONAL AI SYSTEM
        </Text>
      </View>

      {/* STATUS */}
      <View style={styles.statusBox}>
        <View style={styles.onlineDot} />

        <View>
          <Text style={styles.statusTitle}>
            SYSTEM ONLINE
          </Text>

          <Text style={styles.statusSub}>
            PC CONNECTION READY
          </Text>
        </View>
      </View>

      {/* CONSOLE */}
      <View style={styles.console}>
        <Text style={styles.consoleTitle}>
          AVAN COMMAND CONSOLE
        </Text>

        <ScrollView
          style={styles.logScroll}
          showsVerticalScrollIndicator={false}
        >
          {logs.map((log, index) => (
            <Text
              key={index}
              style={styles.consoleLine}
            >
              {log}
            </Text>
          ))}
        </ScrollView>
      </View>

      {/* COMMAND INPUT */}
      <View style={styles.inputContainer}>
        <Text style={styles.prompt}>
          {'>'}
        </Text>

        <TextInput
          value={command}
          onChangeText={setCommand}
          placeholder="Type a command..."
          placeholderTextColor="#426060"
          style={styles.input}
          returnKeyType="send"
          onSubmitEditing={sendCommand}
          editable={!sending}
        />

        <Pressable
          style={[
            styles.sendButton,
            sending && styles.sendButtonDisabled,
          ]}
          onPress={sendCommand}
          disabled={sending}
        >
          <Text style={styles.sendText}>
            {sending ? '...' : 'SEND'}
          </Text>
        </Pressable>
      </View>

      {/* VOICE - LATER */}
      <Pressable
        style={styles.voiceButton}
        onPress={() =>
          setLogs((prev) => [
            ...prev,
            '> Voice system coming soon...',
          ])
        }
      >
        <Text style={styles.mic}>
          ●
        </Text>

        <Text style={styles.voiceText}>
          VOICE COMMAND
        </Text>
      </Pressable>

      {/* FOOTER */}
      <Text style={styles.footer}>
        AVAN REMOTE CONTROL • v1.0
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#050909',
    paddingHorizontal: 20,
    paddingTop: 55,
  },

  header: {
    alignItems: 'center',
    marginBottom: 30,
  },

  logo: {
    color: '#00ffcc',
    fontSize: 38,
    fontWeight: '900',
    letterSpacing: 6,
  },

  subtitle: {
    color: '#426060',
    fontSize: 11,
    letterSpacing: 3,
    marginTop: 6,
  },

  statusBox: {
    flexDirection: 'row',
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#00cc88',
    borderRadius: 10,
    padding: 16,
    backgroundColor: '#071411',
  },

  onlineDot: {
    width: 11,
    height: 11,
    borderRadius: 6,
    backgroundColor: '#00ff99',
    marginRight: 13,
  },

  statusTitle: {
    color: '#00ff99',
    fontSize: 15,
    fontWeight: '800',
  },

  statusSub: {
    color: '#557777',
    fontSize: 10,
    marginTop: 4,
  },

  console: {
    marginTop: 25,
    height: 180,
    borderWidth: 1,
    borderColor: '#183b38',
    borderRadius: 10,
    padding: 16,
    backgroundColor: '#020606',
  },

  consoleTitle: {
    color: '#00aa88',
    fontSize: 11,
    fontWeight: '800',
    letterSpacing: 1.5,
    marginBottom: 15,
  },

  logScroll: {
    flex: 1,
  },

  consoleLine: {
    color: '#608b86',
    fontSize: 12,
    marginBottom: 9,
    fontFamily: 'monospace',
  },

  inputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 22,
    borderWidth: 1,
    borderColor: '#00aa88',
    borderRadius: 9,
    backgroundColor: '#07100f',
    paddingLeft: 12,
  },

  prompt: {
    color: '#00ffcc',
    fontSize: 18,
    fontWeight: 'bold',
  },

  input: {
    flex: 1,
    color: '#d9ffff',
    fontSize: 14,
    paddingHorizontal: 10,
    paddingVertical: 13,
  },

  sendButton: {
    backgroundColor: '#00aa88',
    paddingHorizontal: 15,
    paddingVertical: 14,
    borderTopRightRadius: 8,
    borderBottomRightRadius: 8,
  },

  sendButtonDisabled: {
    opacity: 0.5,
  },

  sendText: {
    color: '#00100c',
    fontSize: 12,
    fontWeight: '900',
  },

  voiceButton: {
    marginTop: 18,
    height: 52,
    borderWidth: 1,
    borderColor: '#00ffcc',
    borderRadius: 9,
    alignItems: 'center',
    justifyContent: 'center',
    flexDirection: 'row',
  },

  mic: {
    color: '#00ffcc',
    fontSize: 16,
    marginRight: 10,
  },

  voiceText: {
    color: '#00ffcc',
    fontSize: 13,
    fontWeight: '800',
    letterSpacing: 2,
  },

  footer: {
    position: 'absolute',
    bottom: 18,
    alignSelf: 'center',
    color: '#294542',
    fontSize: 9,
    letterSpacing: 1.5,
  },
});