# Face Recognition Lock
Door lock with unlocking based on facial recognition results (from the entrance camera)

The door is closed with an electric lock, which can be opened using a relay.

The control elements on the panel in front of the door are a button, a signal speacker and camera lens

After pressing the button, a photo of the person standing in front of the door is taken by the camera and a short buzzer sounds. After this, the controller is compared with a reference face using a facial recognition system based on a neural network. Recognition takes from 1 to 2 seconds (depending on how well the system is trained)

If the person matches with a sufficient degree of reliability, a command is sent to the relay that opens the lock. This is accompanied by playing an audio recording indicating that the face has been recognized.

If a face is not recognized or does not match the reference one and prohibitive audio recording is played

## System installation
To install system on Raspberry Pi up to date Raspbian system (based on Debian distributive) need to be downloaded from [Official operating system images](https://www.raspberrypi.com/software/operating-systems/)

After downloading OS image need to be installed on SD card (4 or 8Gb) using Raspberry [Pi Imager](https://www.raspberrypi.com/software/ or using `sudo apt install rpi-imager`) command in Terminal window
Following commands need to be run on controller after system installation:

```
$ sudo apt-get update
$ sudo apt-get install python-rpi.gpio python3-rpi.gpio
$ sudo apt-get install python-dev python3-dev
$ sudo apt-get install mercurial
$ sudo apt-get install python-pip python3-pip
$ sudo apt-get remove python-rpi.gpio python3-rpi.gpio
$ sudo pip install hg+http://hg.code.sf.net/p/raspberry-gpio-python/code#egg=RPi.GPIO
$ sudo pip-3.2 install hg+http://hg.code.sf.net/p/raspberry-gpio-python/code#egg=RPi.GPIO
$ git clone https://github.com/tylerwowen/RPIO.git
$ cd RPIO
$ sudo python setup.py install
sudo apt-get install build-essential
wget http://www.cmake.org/files/v3.2/cmake-3.2.2.tar.gz
tar xf cmake-3.2.2.tar.gz
cd cmake-3.2.2
./configure
make
```
All scripts need to be copied in `/home/pi/FaceRecognitionLock/` folder

Audio samples for system for sound accompaniment need to be uploaded in `/home/pi/FaceRecognitionLock/audio` folder

* `SoundError.mp3` – the recording is played if there are problems during system initialization or facenot find in frame from camera (There are no faces in the frame, insufficient lighting or problems with the camera)
* `SoundLocked.mp3` – the recording is played if face was recognized but not compare with the correct one
* `SoundOpen.mp3`– the recording is played if face was recognized and matches the correct

## Libraries and Script list

System based on Raspberry Pi Face Recognition Treasure Box (Copyright 2013 Tony DiCola) and use `OpenCV` and `pygame` for work with images by neural network.

System is using `cv2, glob, os, sys, select, config, face, hardware, RPIO, pygame, subprocess, time` libraries.

Main scripts for system work:
* `mainscript.py` – main script which include face recognition and lock opening functions;
* `config.py` - system configuration, includes pins and THRESHOLD variables;
* `relayON.py` – opening electric lock by applying positive voltage to relay, connected to digital pin;
* `relayOFF.py`– closing electric lock by applying negative voltage (connect to ground by pulldown resistor) to relay, connected to digital pin;
* `capture-positives.py` - Start capturing “correct” faces. while the script is running, when you press the enter button, the camera will take a photo, detect faces in it and save them for the next training as “correct”;
* `train.py` – start training a neural network based on previously taken “correct” face images;
* `picam.py` – includes Pi camera device capture class for OpenCV.  This class allows you to capture asingle image from the pi camera as an OpenCV image;
* `face.py` – Face Detection Helper Functions to help with the detection and cropping of faces;
* `hardware.py` – Includes a `box` class that includes functions for working with connected hardware (camera, button and relay connected to the corresponding Raspberry pins);


## System training
The system works using a trained neural network, so before operation it must be configured (trained) for a specific person.

To do this, you need to use a set of photographs of a reference face, taken from the same angle and with the same illumination, as shown by the door camera. The larger the set of reference photographs, the better the recognition result. But with a large number (more than 100), recognition begins to take longer due to controller performance limitations. Optimal amount determined during testing is 30-50 photos, which allows recognition within a comfortable 1-2 seconds.

To capture examples of correct photo `/home/pi/FaceRecognitionLock/capture-positives.py` script need to be run. while the script is running, when you press the enter button, the camera will take a photo, detect faces in it and save them for the next training as “correct”.

The recognition accuracy is separately adjusted by POSITIVE_THRESHOLD constant on which will depend on what maximum difference from the standard is allowed for the system to operate. If the accuracy is too high, the system will only work if there is a complete match, which will require each time to accurately position the face in front of the camera, have the same lighting, facial expression, etc.

Lower accuracy will make the system more convenient to use, but will increase the risk of triggering similar faces. If the accuracy is too low, the system can generally work on any person.

To change value `/home/pi/FaceRecognitionLock/config.py` script need to be manually edited
After capturing set of “correct” photos system need to be trained by running `/home/pi/FaceRecognitionLock/train.py`. Training takes a relatively long time - for a set of 50 correct photos, training takes about 15 minutes (due to the limited power of the controller processor).

The training result is saved as a set of pgm files in `/home/pi/FaceRecognitionLock/training/` folder.

After completing the training, you need to run the main script `/home/pi/FaceRecognitionLock/mainscript.py`  which will be responsible for starting face recognition by pressing a button

To allow main script automatically run after controller is rebooted, the script is registered as a service `mainscriptserv`
```sudo service mainscript.py stop
cd /home/pi/FaceRecognitionLock/
sudo python mainscript.py
sudo service mainscriptserv start```

## Main script logic
Main script `mainscript.py` running after startup as `mainscriptserv` service.

Mainscript initialize standard libraries (include RPIO and pygame)

Pygame initialize and load training data into model. If initialization not succsefull `SoundError.mp3` sound playing

After initialization camera and box class a command is sent to close the lock (if it was open when the system started.) by running `relayOFF.py` script

After unlock button pressed camera take a photo, convert it into grayscale and seachh for coordinates of visible face. If face can’t be found (there are no faces in the frame, insufficient lighting or problems with the camera) `SoundError.mp3` sound playing.

Area where system find face cropped from main image and transfer into trained model to compare with “correct”.

If degree of similarity is insufficient – `SoundLocked.mp3` sound played.

If the degree of similarity is greater than the limit specified by the `POSITIVE_THRESHOLD` variable – `SoundOpen.mp3` sound played and the door opens by running `relayON.py` script. Lock opening for short period (5 seconds by default) after that again you need to recognize the face.

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
- [ ] Connecting to smart home functions
- [ ] Adding video surveillance functions - recording video when trying to open the door or when movement appears in the frame
- [ ] Increasing complexity of the recognition system using video instead of photos, which will not allow using photographs to deceive the system
 
Photos

 
 
 
