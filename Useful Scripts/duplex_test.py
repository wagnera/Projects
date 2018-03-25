#!/usr/bin/env python
import serial
import thread
import time



class rfd900_handler:

	def __init__(self):
		self.s=serial.Serial('/dev/ttyUSB0',57600)
		self.s.reset_input_buffer()
		self.write_timer=time.time()
		self.serial_buffer=""
		self.data=""

	def read(self):
		current_read=''
		current_read=self.s.read(self.s.inWaiting())
		self.serial_buffer=self.serial_buffer + current_read

		while self.serial_buffer.find('\n') > 0:
			self.data,self.serial_buffer=self.serial_buffer.split('\n',1)
			print("complet packet: ",self.data) 
			
	def write(self):
		self.s.write(bytes('123456789')+'\n')
		self.write_timer=time.time()+0.001

	def serial_spinner(self):
		while 1:

			if self.s.inWaiting() > 0:
				self.read()
			if self.write_timer < time.time():
				self.write()

		
a=rfd900_handler()
a.serial_spinner()
