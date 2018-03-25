import serial
import time
ser = serial.Serial('/dev/ttyUSB0', 38400) #Tried with and without the last 3 parameters, and also at 1Mbps, same happens.
#ser.rtscts=False
#ser.dsrdtr=False
ser.flushInput()
ser.flushOutput()
#ser.write("unlogall\r")
#ser.write(b'log gpgga ontime 0.05\r')
#ser.write('log gprmc ontime 0.05\r'.encode())
#ser.write("log bestposa ontime 0.05\r".encode())
#ser.write("log timea ontime 1\r".encode())
#ser.write("log rangea ontime 1\r".encode())
#ser.write("log corrimudata ontime 0.01\r".encode())
while True:
  #ser.write("log rxstatus once\n\n")
  #ser.write(ba)
  data_raw = ser.readline()
  print(data_raw)
  
  #ser.write("log rxstatus once\n\n")
  #time.sleep(0.1)
