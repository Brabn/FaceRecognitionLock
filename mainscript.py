"""
Face Recognition Lock 
Main script

Based on Raspberry Pi Face Recognition Treasure Box
Copyright 2013 Tony DiCola 
"""
import cv2
import glob
import os
import sys
import select
import config
import face
import hardware
import RPIO
import pygame
import subprocess 
import time

if __name__ == '__main__':
	# Load training data into model
	pygame.mixer.init(44100,-16, 300, 1024)
	pygame.mixer.music.load("/home/pi/FaceRecognitionLock/audio/SoundError.mp3")
	pygame.mixer.music.play()
	while pygame.mixer.music.get_busy() == True:
   		continue
	pygame.mixer.music.stop()
	print 'Loading training data...'
	model = cv2.createEigenFaceRecognizer()
	model.load(config.TRAINING_FILE)
	print 'Training data loaded!'
	# Initialize camer and box.
	camera = config.get_camera()
	box = hardware.Box()
	# Move box to locked position.
	box.lock()
	pygame.mixer.music.load("/home/pi/FaceRecognitionLock/audio/SoundError.mp3")
	pygame.mixer.music.play()
	while pygame.mixer.music.get_busy() == True:
   		continue
	pygame.mixer.music.stop()
	print 'Running box...'
	print 'Press button to lock (if unlocked), or unlock if the correct face is detected.'
	print 'Press Ctrl-C to quit.'
	try:
		while True:
			# Check if capture should be made.
			# TODO: Check if button is pressed.
			if box.is_button_up():
				if not box.is_locked:
					# Lock the box if it is unlocked
					box.lock()
					print 'Box is now locked.'
				else:
					print 'Button pressed, looking for face...'
					# Check for the positive face and unlock if found.
					image = camera.read()
					# Convert image to grayscale.
					image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
					# Get coordinates of single face in captured image.
					result = face.detect_single(image)
					if result is None:
						print 'Could not detect single face!  Check the image in capture.pgm' \
							  ' to see what was captured and try again with only one face visible.'
						pygame.mixer.music.load("/home/pi/FaceRecognitionLock/audio/SoundError.mp3")
						pygame.mixer.music.play()
						while pygame.mixer.music.get_busy() == True:
   							continue
						pygame.mixer.music.stop()
						print 'Did not recognize face!'
						continue
					x, y, w, h = result
					# Crop and resize image to face.
					crop = face.resize(face.crop(image, x, y, w, h))
					# Test face against model.
					label, confidence = model.predict(crop)
					print 'Predicted {0} face with confidence {1} (lower is more confident).'.format(
						'POSITIVE' if label == config.POSITIVE_LABEL else 'NEGATIVE', 
						confidence)
					if label == config.POSITIVE_LABEL and confidence < config.POSITIVE_THRESHOLD:
						print 'Recognized face!'
						pygame.mixer.music.load("/home/pi/FaceRecognitionLock/audio/SoundOpen.mp3")
						pygame.mixer.music.play()
						while pygame.mixer.music.get_busy() == True:
   							continue
						pygame.mixer.music.stop()

						box.unlock()
						time.sleep(5)
						box.lock()
  
  
					else:
						pygame.mixer.music.load("/home/pi/FaceRecognitionLock/audio/SoundLocked.mp3")
						pygame.mixer.music.play()
						while pygame.mixer.music.get_busy() == True:
   							continue
						pygame.mixer.music.stop()
						print 'Did not recognize face!'
	except KeyboardInterrupt:
  		RPIO.cleanup()
	RPIO.cleanup()