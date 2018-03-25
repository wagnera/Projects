#!/usr/bin/env python
import pynmea2
import serial
import os
import time

s=serial.Serial('/dev/ttyUSB0',9600)
timer=time.time() + 5

while 1:
	nmea_seq=s.readline()
	try:
		msg=pynmea2.parse(nmea_seq)
		#print(msg)
		#print(msg.latitude,msg.longitude)
		if timer < time.time():
			command = 'ax25beacon -s KN4GQL-7 -c [ -p WIDE1-1 -p WIDE2-1 -- ' + str(msg.latitude) + ' ' + str(msg.longitude) + ' 0'
			#command = 'ax25beacon -s KN4GQL-7 -c > -p WIDE1-1 -p WIDE2-1 -- ' + str(msg.latitude) + ' ' + str(msg.longitude) + ' 0'
			print(command)
			os.system(command)
			timer=time.time() + 60
		else:
			print("Time Reimaing: {time_rem}".format(time_rem=int(timer-time.time())))
			#print(int(timer-time.time()))
	except pynmea2.ParseError:
		pass
	except AttributeError:
		pass