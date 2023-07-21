import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';

const HomePage = () => {
  const handleViewHistory = () => {
  };

  const handleRedirectToCamera = () => {

  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>
        Hello, welcome to surf an amazing application to help you surf throughout your journey of emotions
      </Text>
      <View style={styles.widgetsContainer}>
        <TouchableOpacity onPress={handleViewHistory} style={styles.widget}>
          <Text style={styles.widgetText}>View History</Text>
        </TouchableOpacity>
        <TouchableOpacity onPress={handleRedirectToCamera} style={styles.widget}>
          <Text style={styles.widgetText}>Redirect to Camera</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 20,
  },
  title: {
    fontSize: 20,
    textAlign: 'center',
    marginBottom: 20,
  },
  widgetsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    width: '100%',
  },
  widget: {
    backgroundColor: '#3498db',
    paddingVertical: 15,
    paddingHorizontal: 30,
    borderRadius: 10,
    marginVertical: 10,
  },
  widgetText: {
    color: 'white',
    fontSize: 18,
    textAlign: 'center',
  },
});

export default HomePage;