"""
Face Recognition Lock 
Box Class

Based on Raspberry Pi Face Recognition Treasure Box
Raspberry Pi Face Recognition Treasure Box
Copyright 2013 Tony DiCola 
"""
import time

import cv2
import RPIO
from RPIO import PWM

import picam
import config
import face
import subprocess
import time



class Box(object):
	"""Class to represent the state and encapsulate access to the hardware of 
	the treasure box."""
	def __init__(self):
		RPIO.cleanup()
		# Initialize lock servo and button.
		RPIO.setup(config.LOCK_SERVO_PIN, RPIO.OUT)
		RPIO.setup(config.BUTTON_PIN, RPIO.IN,  pull_up_down = RPIO.PUD_UP)
		# Set initial box state.
		self.button_state = RPIO.input(config.BUTTON_PIN)
		self.is_locked = None

	def lock(self):
		"""Lock the box."""
		subprocess.Popen("sudo python /home/pi/FaceRecognitionLock/relayOFF.py", shell=True)
		self.is_locked = True

	def unlock(self):
		"""Unlock the box."""
		subprocess.Popen("sudo python /home/pi/FaceRecognitionLock/relayON.py", shell=True)
		time.sleep(5)
		subprocess.Popen("sudo python /home/pi/FaceRecognitionLock/relayOFF.py", shell=True)
		self.is_locked = False

	def is_button_up(self):
		"""Return True when the box button has transitioned from down to up (i.e.
		the button was pressed)."""
		old_state = self.button_state
		self.button_state = RPIO.input(config.BUTTON_PIN)
		# Check if transition from down to up
		if old_state == config.BUTTON_DOWN and self.button_state == config.BUTTON_UP:
			# Wait 20 milliseconds and measure again to debounce switch.
			time.sleep(20.0/1000.0)
			self.button_state = RPIO.input(config.BUTTON_PIN)
			if self.button_state == config.BUTTON_UP:
				return True
		return False
