import React from 'react';
import { View, StyleSheet } from 'react-native';
import HomePage from './HomePage';

const App = () => {
  return (
    <View style={styles.container}>
      <HomePage />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
});

export default App;