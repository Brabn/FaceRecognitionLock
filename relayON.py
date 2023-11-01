#Face Recognition Lock 
# Script for switching on relay

import config
import RPIO

if __name__ == '__main__':
	try:
		#print 'Relay ON'
		RPIO.setwarnings(False)
		RPIO.cleanup() 
		RPIO.setup(config.LOCK_PIN, RPIO.OUT)
	except KeyboardInterrupt:
  		RPIO.cleanup()
	#RPIO.cleanup()