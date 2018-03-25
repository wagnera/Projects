from dronekit import connect, VehicleMode
from pymavlink import mavutil
import time

vehicle = connect('/dev/ttyACM0', wait_ready=True)
SWITCH=False

msg_lower_load = vehicle.message_factory.command_long_encode(
    0, 0,    # target system, target component
    mavutil.mavlink.MAV_CMD_DO_SET_SERVO, #command
    0, #confirmation
    8,    # param 1, Servo number
    1500,          # PWM value
    0,          # param 3
    0, # param 4
    0, 0, 0)    # param 5 ~ 7 not used

msg_retract_load = vehicle.message_factory.command_long_encode(
    0, 0,    # target system, target component
    mavutil.mavlink.MAV_CMD_DO_SET_SERVO, #command
    0, #confirmation
    8,    # param 1, Servo number
    1900,          # PWM value
    0,          # param 3
    0, # param 4
    0, 0, 0)    # param 5 ~ 7 not used

msg_hold_load= vehicle.message_factory.command_long_encode(
    0, 0,    # target system, target component
    mavutil.mavlink.MAV_CMD_DO_SET_SERVO, #command
    0, #confirmation
    8,    # param 1, Servo number
    1550,          # PWM value
    0,          # param 3
    0, # param 4
    0, 0, 0)    # param 5 ~ 7 not used

msg_lower_noload = vehicle.message_factory.command_long_encode(
    0, 0,    # target system, target component
    mavutil.mavlink.MAV_CMD_DO_SET_SERVO, #command
    0, #confirmation
    8,    # param 1, Servo number
    1400,          # PWM value
    0,          # param 3
    0, # param 4
    0, 0, 0)    # param 5 ~ 7 not used

msg_hold_noload= vehicle.message_factory.command_long_encode(
    0, 0,    # target system, target component
    mavutil.mavlink.MAV_CMD_DO_SET_SERVO, #command
    0, #confirmation
    8,    # param 1, Servo number
    1530,          # PWM value
    0,          # param 3
    0, # param 4
    0, 0, 0)    # param 5 ~ 7 not used

def channels_callback(self, attr_name,value):
	#print(attr_name,value['6'])
	if value['6'] <1500:
		global SWITCH
		SWITCH=True
		#print(SWITCH)
	if value['6'] >=1500:
		global SWITCH
		SWITCH=False
		#print(SWITCH)


vehicle.add_attribute_listener('channels', channels_callback)
vehicle.send_mavlink(msg_hold_noload)
print("waiing for user to command retract")
while (SWITCH==False):
	time.sleep(0.1)

print("retracting")
vehicle.send_mavlink(msg_retract_load)	
while (SWITCH):
	time.sleep(0.1)
print("Ready")
vehicle.send_mavlink(msg_hold_load)
while (SWITCH==False):
	time.sleep(0.1)

print("lowering")
vehicle.send_mavlink(msg_lower_load)
time.sleep(10)
print("flying mission")
vehicle.send_mavlink(msg_hold_load)
while (SWITCH):
	time.sleep(0.1)
print("lowering with load")
vehicle.send_mavlink(msg_lower_load)
time.sleep(5)
print("final release")
vehicle.send_mavlink(msg_lower_noload)
time.sleep(5)
print("reset")
vehicle.send_mavlink(msg_hold_noload)
vehicle.close()