import serial
import time
import string
ser = serial.Serial('/dev/ttyACM0', 115200) #Tried with and without the last 3 parameters, and also at 1Mbps, same happens.
ser.xonxoff=True
ser.parity=serial.PARITY_NONE
ser.flushInput()
ser.flushOutput()
data_buff=list()
num_avg=1
f=open('range_data.txt','w')
if f:
	print('file opened')
while True:

  for ii in range(num_avg):
  	temp_data=ser.readline()
  	temp_data = string.replace(temp_data,'\n','')
  	temp_data = string.replace(temp_data,'\r','')
  	data_buff.append(temp_data)
  
  sum=0
  for ii in range(num_avg):
  	sum=sum+int(data_buff[ii])
  avg=sum/num_avg
  print(avg)
  f.write(str(avg))
  f.write(',')
  data_buff=list()
