#!/usr/bin/python
import rospy
import click
import math
import actionlib
import tf

from geographiclib.geodesic import Geodesic
from actionlib_msgs.msg import GoalStatus
from geometry_msgs.msg import PoseStamped,Vector3Stamped,PointStamped
from sensor_msgs.msg import NavSatFix, Imu
from visualization_msgs.msg import Marker
def DMS_to_decimal_format(lat,long):
  # Check for degrees, minutes, seconds format and convert to decimal
  if ',' in lat:
    degrees, minutes, seconds = lat.split(',')
    degrees, minutes, seconds = float(degrees), float(minutes), float(seconds)
    if lat[0] == '-': # check for negative sign
      minutes = -minutes
      seconds = -seconds
    lat = degrees + minutes/60 + seconds/3600
  if ',' in long:
    degrees, minutes, seconds = long.split(',')
    degrees, minutes, seconds = float(degrees), float(minutes), float(seconds)
    if long[0] == '-': # check for negative sign
      minutes = -minutes
      seconds = -seconds
    long = degrees + minutes/60 + seconds/3600

  lat = float(lat)
  long = float(long)
  rospy.loginfo('Given GPS goal: lat %s, long %s.' % (lat, long))
  return lat, long

def get_origin_lat_long():
  # Get the lat long coordinates of our map frame's origin which must be publshed on topic /local_xy_origin. We use this to calculate our goal within the map frame.
  rospy.loginfo("Waiting for a message to initialize the origin GPS location...")
  origin_pose = rospy.wait_for_message('local_xy_origin', PoseStamped)
  origin_lat = origin_pose.pose.position.y
  origin_long = origin_pose.pose.position.x
  rospy.loginfo('Received origin: lat %s, long %s.' % (origin_lat, origin_long))
  return origin_lat, origin_long

def calc_goal(origin_lat, origin_long, goal_lat, goal_long):
  # Calculate distance and azimuth between GPS points
  geod = Geodesic.WGS84  # define the WGS84 ellipsoid
  g = geod.Inverse(origin_lat, origin_long, goal_lat, goal_long) # Compute several geodesic calculations between two GPS points 
  hypotenuse = distance = g['s12'] # access distance
  rospy.loginfo("The distance from the origin to the goal is {:.3f} m.".format(distance))
  azimuth = g['azi1']
  rospy.loginfo("The azimuth from the origin to the goal is {:.3f} degrees.".format(azimuth))

  # Convert polar (distance and azimuth) to x,y translation in meters (needed for ROS) by finding side lenghs of a right-angle triangle
  y = adjacent = math.cos(math.radians(azimuth)) * hypotenuse
  x = opposite = math.sin(math.radians(azimuth)) * hypotenuse
  rospy.loginfo("The translation from the origin to the goal is (x,y) {:.3f}, {:.3f} m.".format(x, y))

  return x, y

class GpsGoal():
  def __init__(self):
    rospy.init_node('gps_goal')
    rospy.Subscriber('gps_goal_pose', PoseStamped, self.gps_goal_pose_callback)
    rospy.Subscriber('gps_goal_fix', NavSatFix, self.gps_goal_fix_callback)
    self.point_pub=rospy.Publisher('/imu_point', PointStamped, queue_size=10)
    self.goal_pub=rospy.Publisher('/survey_markers', Marker, queue_size = 10)
    # Get the lat long coordinates of our map frame's origin which must be publshed on topic /local_xy_origin. We use this to calculate our goal within the map frame.
    self.origin_lat, self.origin_long = get_origin_lat_long()
    self.id = 0

  def do_gps_goal(self, goal_lat, goal_long, z=0, yaw=0, roll=0, pitch=0):
    # Calculate goal x and y in the frame_id given the frame's origin GPS and a goal GPS location
    x, y = calc_goal(self.origin_lat, self.origin_long, goal_lat, goal_long)
    # Create move_base goal
    self.publish_goal(x=x, y=y, z=z, yaw=yaw, roll=roll, pitch=pitch)

  def gps_goal_pose_callback(self, data):
    lat = data.pose.position.y
    long = data.pose.position.x
    z = data.pose.position.z
    euler = tf.transformations.euler_from_quaternion(data.pose.orientation)
    roll = euler[0]
    pitch = euler[1]
    yaw = euler[2]
    self.do_gps_goal(lat, long, z=z, yaw=yaw, roll=roll, pitch=pitch)

  def gps_goal_fix_callback(self, data):
    self.do_gps_goal(data.latitude, data.longitude)

  def publish_goal(self, x=0, y=0, z=0, yaw=0, roll=0, pitch=0):
    # Create move_base goal
    marker = Marker()
    marker.header.stamp = rospy.Time.now()
    marker.ns = 'test'
    marker.type = 2
    marker.id = self.id
    size = 0.2
    marker.scale.x=size
    marker.scale.y=size
    marker.scale.z=size
    marker.color.r = 0.8
    marker.color.a = 1.0
    marker.header.frame_id = rospy.get_param('~frame_id','map')
    marker.pose.position.x = x
    marker.pose.position.y = y
    marker.pose.position.z =  z
    quaternion = tf.transformations.quaternion_from_euler(roll, pitch, yaw)
    marker.pose.orientation.x = quaternion[0]
    marker.pose.orientation.y = quaternion[1]
    marker.pose.orientation.z = quaternion[2]
    marker.pose.orientation.w = quaternion[3]
    rospy.loginfo('Executing move_base goal to position (x,y) %s, %s, with %s degrees yaw.' %
            (x, y, yaw))
    rospy.loginfo("To cancel the goal: 'rostopic pub -1 /move_base/cancel actionlib_msgs/GoalID -- {}'")

    # Send goal
    #print(marker)
    self.goal_pub.publish(marker)

@click.command()
@click.option('--lat', prompt='Latitude', help='Latitude')
@click.option('--long', prompt='Longitude', help='Longitude')
@click.option('--roll', '-r', help='Set target roll for goal', default=0.0)
@click.option('--pitch', '-p', help='Set target pitch for goal', default=0.0)
@click.option('--yaw', '-y', help='Set target yaw for goal', default=0.0)
def cli_main(lat, long, roll, pitch, yaw):
  """Send goal to move_base given latitude and longitude

  \b
  Two usage formats:
  gps_goal.py --lat 43.658 --long -79.379 # decimal format
  gps_goal.py --lat 43,39,31 --long -79,22,45 # DMS format
  """
  gpsGoal = GpsGoal();

  # Check for degrees, minutes, seconds format and convert to decimal
  lat, long = DMS_to_decimal_format(lat, long)
  gpsGoal.do_gps_goal(lat, long, roll=roll, pitch=pitch, yaw=yaw)


def ros_main():
  gpsGoal = GpsGoal();
  r = rospy.Rate(1)
  while not rospy.is_shutdown():
    gpsGoal.do_gps_goal(37.1966381229321000, -80.5793958729490000)
    gpsGoal.id += 1
    gpsGoal.do_gps_goal(37.1965814970194000, -80.5790738173803000)
    gpsGoal.id += 1
    gpsGoal.do_gps_goal(37.1966908659093000, -80.5792458251302000) 
    gpsGoal.id += 1
    gpsGoal.do_gps_goal(37.1965513259304000, -80.5794927350731000)
    r.sleep() 


if __name__ == '__main__':
  ros_main()
  #cli_main()