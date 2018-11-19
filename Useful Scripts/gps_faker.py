from sensor_msgs.msg import NavSatFix
import rospy, time
rospy.init_node('gps_faker')
nav_pub=rospy.Publisher('fix', NavSatFix, queue_size=10)
lat=38.405144
lon=-110.792672
while not rospy.is_shutdown():
	data=NavSatFix()
	data.latitude=lat#38.405144
	data.longitude=lon#-110.792672
	#lat+=0.0001
	#lon+=0.0001
	nav_pub.publish(data)
	time.sleep(1)