import thingspeak
import time
import sys
import Adafruit_DHT
import RPi.GPIO as GPIO
from mq import *

#parameters
channel_id = 770161
write_key  = '7FA8M36YRY1IHH1V'
read_key   = 'DC0NWROA3XOXMC09'
pin = 4
sensor = Adafruit_DHT.DHT11
mq = MQ();

#define function
def measure(channel):
	try:
		#read humidity and Temperature
		humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
		# read
		read = channel.get({})
		print("Read:", read)

		#Lights on/off accordingly to Temperatures
		#GPIO. is the first part of the control for raspberry's gpio pins
		if temperature < 25:
			GPIO.setmode(GPIO.BCM)
			GPIO.setwarnings(False)
			GPIO.setup(16,GPIO.OUT) #16 = GREEN
			print("LED on")
			GPIO.output(16,GPIO.HIGH)
			time.sleep(10)
			print("LED off")
			GPIO.output(16,GPIO.LOW)
		elif temperature > 25: #26 = YELLOW
			GPIO.setmode(GPIO.BCM)
			GPIO.setwarnings(False)
			GPIO.setup(26,GPIO.OUT)
			print("LED on")
			GPIO.output(26,GPIO.HIGH)
			time.sleep(10)
			print("LED off")
			GPIO.output(26,GPIO.LOW)
		elif temperature > 30: # 21 = RED
			GPIO.setmode(GPIO.BCM)
			GPIO.setwarnings(False)
			GPIO.setup(21,GPIO.OUT)
			print("LED on")
			GPIO.output(21,GPIO.HIGH)
			time.sleep(10)
			print("LED off")
			GPIO.output(21,GPIO.LOW)
		#Air Quality Sensor
		#Show Measurement-Values
		perc = mq.MQPercentage()
		sys.stdout.write("\r")
		sys.stdout.write("\033[K")
		sys.stdout.write("LPG: %g ppm, CO: %g ppm, Smoke:%g ppm" % (perc["GAS_LPG"],perc["CO"],perc["SMOKE"]))
		response = channel.update({'field1': temperature, 'field2': humidity, 'field3': (perc["CO"]*100000)})

	except Exception as e:
        	print(e)

#start main program
if __name__ == "__main__":
#Connect to API channel
    channel = thingspeak.Channel(id=channel_id, write_key=write_key, api_key=read_key)
    while True:
	print("Function:")
        measure(channel)
        # free account has an api limit of 15sec
        time.sleep(15)
