import thingspeak
import time
import sys
import Adafruit_DHT
import RPi.GPIO as GPIO
import mysql.connector
from mysql.connector import Error
from mq import *


channel_id = 770161
# add real keys
write_key  = 'x'
read_key   = 'x'
pin = 4
sensor = Adafruit_DHT.DHT11
mq = MQ();

def measure(channel):
	try:
        #add real connection
		connection = mysql.connector.connect(host='x',
				database='x',
				user='x',
				password='x')
		if connection.is_connected():
			 sql_select_Query = "select * from bordevalues"
			 cursor = mySQLconnection .cursor()
			 cursor.execute(sql_select_Query)
			 records = cursor.fetchall()
			print("Total number of rows in Database  is - ", cursor.rowcount)
			for row in records:

		try:
		        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
		        # read
		        read = channel.get({})
		        print("Read:", read)

			if temperature < row[2]:
				GPIO.setmode(GPIO.BCM)
				GPIO.setwarnings(False)
				GPIO.setup(16,GPIO.OUT) #16 = GREEN
				print("LED on")
				GPIO.output(16,GPIO.HIGH)
				time.sleep(10)
				print("LED off")
				GPIO.output(16,GPIO.LOW)
			elif temperature > row[1]: #26 = YELLOW
				GPIO.setmode(GPIO.BCM)
				GPIO.setwarnings(False)
				GPIO.setup(26,GPIO.OUT)
				print("LED on")
				GPIO.output(26,GPIO.HIGH)
				time.sleep(10)
				print("LED off")
				GPIO.output(26,GPIO.LOW)
			elif temperature > row[0]: # 21 = RED
				GPIO.setmode(GPIO.BCM)
				GPIO.setwarnings(False)
				GPIO.setup(21,GPIO.OUT)
				print("LED on")
				GPIO.output(21,GPIO.HIGH)
				time.sleep(10)
				print("LED off")
				GPIO.output(21,GPIO.LOW)
			#Air Quality Sensor
			perc = mq.MQPercentage()
			sys.stdout.write("\r")
			sys.stdout.write("\033[K")
			sys.stdout.write("LPG: %g ppm, CO: %g ppm, Smoke:%g ppm" % (perc["GAS_LPG"],perc["CO"],perc["SMOKE"]))
			response = channel.update({'field1': temperature, 'field2': humidity, 'field3': (perc["CO"]*100000)})
		cursor.close()
		except Exception as e:
		        	print(e)
				cursor.close()
	except Error as e :
	    print ("Error while connecting to MySQL", e)
	finally:
		    #closing database connection.
		    if(connection.is_connected()):
		        cursor.close()
		        connection.close()
		        print("MySQL connection is closed")

if __name__ == "__main__":
    channel = thingspeak.Channel(id=channel_id, write_key=write_key, api_key=read_key)
    while True:
	print("Function:")
        measure(channel)
        # free account has an api limit of 15sec
        time.sleep(15)
