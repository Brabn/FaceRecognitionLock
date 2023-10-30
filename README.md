# Face Recognition Lock
Door lock with unlocking based on facial recognition results (from the entrance camera)

The door is closed with an electric lock, which can be opened using a relay.

The control elements on the panel in front of the door are a button, a signal speacker and camera lens

After pressing the button, a photo of the person standing in front of the door is taken by the camera and a short buzzer sounds. After this, the controller is compared with a reference face using a facial recognition system based on a neural network. Recognition takes from 1 to 2 seconds (depending on how well the system is trained)

If the person matches with a sufficient degree of reliability, a command is sent to the relay that opens the lock. This is accompanied by playing an audio recording indicating that the face has been recognized.

If a face is not recognized or does not match the reference one and prohibitive audio recording is played

## System training
The system works using a trained neural network, so before operation it must be configured (trained) for a specific person.

To do this, you need to use a set of photographs of a reference face, taken from the same angle and with the same illumination, as shown by the door camera. The larger the set of reference photographs, the better the recognition result. But with a large number (more than 100), recognition begins to take longer due to controller performance limitations. Optimal amount determined during testing is 30-50 photos, which allows recognition within a comfortable 1-2 seconds.

The recognition accuracy is separately adjusted - a certain coefficient on which will depend on what maximum difference from the standard is allowed for the system to operate. If the accuracy is too high, the system will only work if there is a complete match, which will require each time to accurately position the face in front of the camera, have the same lighting, facial expression, etc. 

Lower accuracy will make the system more convenient to use, but will increase the risk of triggering similar faces. If the accuracy is too low, the system can generally work on any person. Therefore, this coefficient must be adjusted before training (adjusted manually in the configuration file).

In a serial version, the neural network is trained using a command to the controller, which will use a photo from the camera. Recognition accuracy can also be adjusted programmatically or using control buttons

## Main system parameters 
* Main controller		Raspberry Pi Zero W
* Main processor		1 GGh, ARM1176JZ-F 
* Graphic processor		VideoCore IV	48+
* Chipset			Broadcom BCM2835 
* RAM				512 Mb DDR2
* Memory			8 Gb (microSD)
* Communication		WiFi 802.11 b/g/n, Bluetooth 4.1
* Connectors			microUSB, miniHDMI
* Camera 			Sony IMX219
* Camera resolution		8 Mp (3280 х 2464)
* Supporting video formats	1080р @ 30fps, 720p @ 60 fps и 640 х 480p @ 90fps
* Matrix size			¼’
* Pixel size			1.4μm х 1.4μm 
* Relay power			 
    - 2.2 kW AC (220 V, 10A)
    - 300 W DC (30 V, 10A)
* Power supply			10W (5V 2A) 


## Components

* Raspberry Pi Zero W
* Paspberry Pi Camera
* SD-card (min 8 Gb)
* 1 channel ralay 300VA (10A 30V)
* Audio speaker with 3.5mm Audio Jack

## Wiring diagram


## Further development of the system
- [ ] Adding a training function without using a pre-selected set of photos - using the built-in door camera by command from the remote control
- [ ] Connecting to smart home functions
- [ ] Adding video surveillance functions - recording video when trying to open the door or when movement appears in the frame
- [ ] Increasing complexity of the recognition system using video instead of photos, which will not allow using photographs to deceive the system
 
Photos

 
 
 
