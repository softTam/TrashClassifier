import React, { useState, useEffect, useRef} from 'react';
import { StyleSheet, Text, View, Image, TouchableOpacity } from 'react-native';
import { Camera, CameraType } from 'expo-camera';
import { Entypo } from '@expo/vector-icons'
import * as MediaLibrary from 'expo-media-library';
import Button from './src/components/Button';

export default function App() {
  const [hasCameraPermission, setHasCameraPermission] = useState(null);
  const [image, setImage] = useState(null);
  const [type, setType] = useState(Camera.Constants.Type.back);
  const [flash, setFlash] = useState(Camera.Constants.FlashMode.off);
  const cameraRef = useRef(null);
  
  useEffect(() => {
    (async () => {
      MediaLibrary.requestPermissionsAsync();
      const cameraStatus = await Camera.requestCameraPermissionsAsync();
      setHasCameraPermission(cameraStatus.status === "granted");
    })();
  }, [])

  if(hasCameraPermission === false) {
    return <Text>No access to camera</Text>
  }

  const takePicture = async () => {
    if(cameraRef) {
      try{
        const data = await cameraRef.current.takePictureAsync();
        console.log(data);
        setImage(data.uri);
        /*
        var photo = {
          uri: data.uri,
          type: 'image/jpeg',
          name: '1.jpg',
        };
        var form = new FormData();
        form.append("Input_Image", photo);
        
        fetch(
          'http://127.0.0.1:8000/upload',
          {
            body: form,
            method: "PUT",
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          }
        ).then((response) => response.json())
        .catch((error) => {
          alert("ERROR " + error)
        })
        .then((responseData) => {
          alert("Succes "+ responseData)
        }).done();*/
      } catch(e) {
        console.log(e);
      }


    }
  }

  /*
    <Camera
        style={styles.camera}
        type={type}
        FlashMode={flash}
        ref={cameraRef}
        >
      </Camera>
      <View>
        <Button title={'Take a picture'} icon="camera" />
      </View>
  */
  return (
    <View style={styles.container}>
      <Image source={require('./assets/icon.png')} style={styles.logo}/>

      <View style={styles.header}>
        <TouchableOpacity style={styles.touchable}>
          <Text>Question?</Text>
        </TouchableOpacity>
      </View>

      <View style={styles.camera_holder}>
        {!image ?
          <Camera style={styles.camera} type={type} FlashMode={flash} ref={cameraRef}>
          </Camera>
          :
          <Image source={{uri: image}} style={styles.camera} />
        }
        <Button title={'Take a picture'} icon="camera" onPress={() => takePicture()}/>
      </View>

    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#d2ffbb',
    padding: 15,
  },

  logo: {
    marginTop: 40,
    width: 50,
    height: 50,
    flexDirection: 'row',
  },

  camera: {
    flex: 0.9,
    borderRadius: 25,
    overflow:'hidden',
    margin: 15
  },

  camera_holder: {
    marginTop: 50,
    flex: 0.75,
    backgroundColor: '#74cb34',
    borderRadius: 20
  },

  image: {
    flex: 1
  },

  header: {
    marginTop: 20,
    flexDirection: 'row'
  },

  touchable: {
    borderWidth: 1
  }
});
