import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';

const HomeScreen = ({ navigation }) => {
  // Dummy data for emotion detection results (replace this with real data)
  const emotionsData = [
    { emotion: 'Happy', percentage: 0.30 },
    { emotion: 'Sad', percentage: 0.12 },
    { emotion: 'Angry', percentage: 0.15 },
    { emotion: 'Disgusting', percentage: 0.20 },
    { emotion: 'Fear', percentage: 0.10 },
    { emotion: 'Neutral', percentage: 0.10 },
    { emotion: 'Surprise', percentage: 0.03 },
  ];

  return (
    <View style={styles.container}>
      <Text style={styles.header}>Surf App</Text>
      <Text style={styles.subHeader}>Detect Emotions and Create Avatars</Text>

      {emotionsData.map((data) => (
        <TouchableOpacity
          key={data.emotion}
          style={styles.widget}
          onPress={() => {
            // Handle navigation or any other action when tapping the widget
          }}
        >
          <Text style={styles.widgetText}>{data.emotion}</Text>
          <Text style={styles.widgetText}>{(data.percentage * 100).toFixed(1)}%</Text>
        </TouchableOpacity>
      ))}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f0f0f0',
  },
  header: {
    fontSize: 32,
    fontWeight: 'bold',
    marginBottom: 20,
  },
  subHeader: {
    fontSize: 18,
    marginBottom: 40,
  },
  widget: {
    backgroundColor: '#fff',
    padding: 15,
    borderRadius: 8,
    marginBottom: 10,
    width: 200,
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  widgetText: {
    fontSize: 16,
  },
  button: {
    backgroundColor: '#007bff',
    padding: 15,
    borderRadius: 8,
  },
  buttonText: {
    color: '#ffffff',
    fontSize: 18,
    fontWeight: 'bold',
  },
});

export default HomeScreen;
