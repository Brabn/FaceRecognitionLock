#Face Recognition Lock 
# Script for switching off relay

import config
import RPIO

if __name__ == '__main__':
	#print 'Relay OFF'
	try:
		RPIO.setwarnings(False) 
		RPIO.setup(config.LOCK_PIN, RPIO.OUT)
		RPIO.cleanup()
	except KeyboardInterrupt:
  		RPIO.cleanup()
	RPIO.cleanup()