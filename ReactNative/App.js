import React, { useState, useEffect, useRef} from 'react';
import { StyleSheet, Text, View, Image, TouchableOpacity, Modal, Animated, TouchableWithoutFeedback } from 'react-native';
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
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [myLabel, setMyLabel] = useState("Few Seconds ...");
  const [mySolution, setMySolution] = useState("")
  functionCombined = () => {
    setIsModalVisible(false);
    setMyLabel('Few seconds ...');
    setMySolution('');
  } 
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
        setIsModalVisible(true);
        const photo = await cameraRef.current.takePictureAsync();
        console.log(photo);

        const image = new FormData();
        image.append("file", {
          name: 'file',
          type: photo.type,
          uri: photo.uri,
        });
        // {"file": photo.uri}
        fetch("https://horrible-octopus-32.loca.lt/media/upload", {
          method: "POST",
          body: image
        })
          .then(response => response.json())
          .then(response => {
            setMyLabel(response['Category'])
            setMySolution(response['Msg'])
            console.log("upload succes", response['Category']);
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
      <Modal visible={isModalVisible} style={styles.modal}>
        <View style={styles.response}>
          <Text style={styles.label}> {myLabel}</Text>
          <Text style={styles.solution}> {mySolution}</Text>
        </View>
          <TouchableOpacity onPress={()=>functionCombined()} style={styles.close_button}>
            <Text>Close</Text>
          </TouchableOpacity>
      </Modal>
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

  close_button: { 
    height: 70,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    marginHorizontal: 50,
    borderRadius: 10,
    borderColor: 'black',
    borderWidth: 1,
    marginTop: 400
  },
  modal: {
    justifyContent: 'center',
    alignItems: 'center',
  },

  label: {
    marginTop: 200,
    fontSize: 50,
    backgroundColor: 'red',
    height: 100,
  },
});
