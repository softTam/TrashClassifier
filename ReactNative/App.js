import React, { useState, useEffect, useRef} from 'react';
import { StyleSheet, Text, View, Image, TouchableOpacity, Modal, Animated } from 'react-native';
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
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    (async () => {
      MediaLibrary.requestPermissionsAsync();
      const cameraStatus = await Camera.requestCameraPermissionsAsync();
      setHasCameraPermission(cameraStatus.status === "granted");
    })();
  }, []);

  if(hasCameraPermission === false) {
    return <Text>No access to camera</Text>
  }

  const takePicture = async () => {
    if(cameraRef) {
      try{
        const photo = await cameraRef.current.takePictureAsync();
        console.log(photo);

        const image = new FormData();
        image.append("file", {
          name: 'file',
          type: photo.type,
          uri: photo.uri,
        });
        // {"file": photo.uri}
        fetch("https://wastewisely.loca.lt/media/upload", {
          method: "POST",
          body: image
        })
          .then(response => response.json())
          .then(response => {
            console.log("upload succes", response);
            this.setState({ photo: null });
          })
          .catch(error => {
          });

        } catch(e) {
          console.log(e);
        }
    }
  }

  return (
    <View style={styles.container}>
      <View style={styles.logos}>
        <Image source={require('./assets/applogo2.png')} style={styles.logo}/>
        <Image source={require('./assets/logowaste3.png')} style={styles.logowaste}/>
      </View>

      <View style={styles.camera_holder}>
        {!image ?
          <Camera style={styles.camera} type={type} FlashMode={flash} ref={cameraRef} autoFocus={Camera.Constants.AutoFocus.on}>
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

  logos: {
    flexDirection:'row', 
    alignItems:'center', 
    justifyContent:'center'
  },

  logo: {
    flex: 1,
    width: 100,
    height: 100,
    flexDirection: 'row',
    marginLeft: 20,
    marginTop: 50
  },

  logowaste: {
    marginTop: 50,
    width: 100,
    height: 110,
    flex: 5,
    flexDirection: 'row',
  },

  camera: {
    flex: 0.9,
    borderRadius: 25,
    overflow:'hidden',
    margin: 15
  },

  camera_holder: {
    marginTop: 30,
    flex: 0.850,
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
  },
});
