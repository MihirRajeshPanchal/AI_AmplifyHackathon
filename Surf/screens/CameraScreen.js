import React, { useState, useEffect, useRef } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Alert } from 'react-native';
import { Camera as ExpoCamera } from 'expo-camera';

const CameraScreen = () => {
  const [hasPermission, setHasPermission] = useState(null);
  const [cameraType, setCameraType] = useState(ExpoCamera.Constants.Type.front);
  const cameraRef = useRef(null);

  useEffect(() => {
    (async () => {
      const { status } = await ExpoCamera.requestPermissionsAsync();
      setHasPermission(status === 'granted');
    })();
  }, []);

  const takePicture = async () => {
    if (cameraRef.current) {
      try {
        const { uri } = await cameraRef.current.takePictureAsync();

        // Send the image URI to the Flask API for processing
        const formData = new FormData();
        const imageUriParts = uri.split('.');
        const imageType = imageUriParts[imageUriParts.length - 1];

        formData.append('image', {
          uri,
          type: `image/${imageType}`, // Use the correct image type based on the image extension
          name: `image.${imageType}`,
        });

        fetch('http://192.160.161.157:5000/compute', {
          method: 'POST',
          body: formData,
        })
          .then((response) => response.json())
          .then((data) => {
            // Handle the response received from the server
            if (data.emotion) {
              Alert.alert('Emotion Detected', `The detected emotion is: ${data.emotion}`);
            } else {
              Alert.alert('Error', 'Error occurred during computation.');
            }
          })
          .catch((error) => {
            console.log('Error sending image:', error);
            Alert.alert('Error', 'Error occurred during image processing.');
          });
      } catch (error) {
        console.log('Error taking picture:', error);
        Alert.alert('Error', 'Error occurred while taking a picture.');
      }
    }
  };

  const switchCamera = () => {
    setCameraType((prevType) =>
      prevType === ExpoCamera.Constants.Type.front
        ? ExpoCamera.Constants.Type.back
        : ExpoCamera.Constants.Type.front
    );
  };

  if (hasPermission === null) {
    return <View />;
  }
  if (hasPermission === false) {
    return <Text>No access to camera</Text>;
  }

  return (
    <View style={styles.container}>
      <ExpoCamera ref={cameraRef} style={styles.camera} type={cameraType} />
      <View style={styles.buttonContainer}>
        <TouchableOpacity style={styles.button} onPress={takePicture}>
          <Text style={styles.buttonText}>Take Picture</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.button} onPress={switchCamera}>
          <Text style={styles.buttonText}>Switch Camera</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    flexDirection: 'column',
    backgroundColor: 'black',
  },
  camera: {
    flex: 1,
  },
  buttonContainer: {
    position: 'absolute',
    bottom: 20,
    left: 0,
    right: 0,
    alignItems: 'center',
  },
  button: {
    backgroundColor: 'white',
    padding: 20,
    borderRadius: 10,
    marginBottom: 10,
  },
  buttonText: {
    fontSize: 18,
    color: 'black',
  },
});

export default CameraScreen;
