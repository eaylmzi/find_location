#! /usr/bin/env python

#Make a python node executable
#chmod u+x ~/catkin_ws/src/beginner_tutorials/src/scanenv1.py

import rospy
import sys
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion,quaternion_from_euler
import math
import time

scanning = 1
rotatecount = 0

class Robot:
	
	def __init__(self,nodeid):
		rospy.init_node('turtletogoal', anonymous=True)
		self.nodename = 'robot_' + nodeid
		self.vel_publisher = rospy.Publisher(self.nodename + '/cmd_vel', Twist, queue_size=10) 
		self.pose_subscriber = rospy.Subscriber(self.nodename +'/odom', Odometry, self.update_pose)
		self.scan_sub = rospy.Subscriber(self.nodename+'/base_scan', LaserScan, self.callback)

		self.odom = Odometry()
		self.pose = self.odom.pose.pose
		self.rate = rospy.Rate(10)
		self.roll = self.pitch = self.yaw = 0.0
	
	def callback(self,msg):
		global scanning
		if(msg.ranges[135] < 0.75):
			scanning = msg.ranges[135]


	def update_pose(self, data):
		global axis_x
		global axis_y
		self.pose = data.pose.pose
	        orientation_q = self.pose.orientation
	        orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
	        (self.roll, self.pitch, self.yaw) = euler_from_quaternion (orientation_list)
		axis_x = self.pose.position.x
		axis_y = self.pose.position.y
		

	def get_position_x(self):
		return self.pose.position.x
	def get_position_y(self):
		return self.pose.position.y

	def movetask(self,scan,count,yamlvalue):
				
		global rotatecount
 		global scanning			
		vel_msg =Twist()
		speed=1
		isforward=1
		distance=0.4
		if isforward == 1:
			vel_msg.linear.x=abs(speed)
		else:
			vel_msg.linear.x=-abs(speed)
		
		if(scan > 0.75):
			
			vel_msg.angular.z=0.0	
			rate= rospy.Rate(10)
			t0=rospy.Time.now().to_sec()
			current_dist=0
			while current_dist < distance:
				self.vel_publisher.publish(vel_msg)
				t1=rospy.Time.now().to_sec()
				current_dist=speed*(t1-t0)
				rate.sleep()
		elif(count % 2 == 0):
			print("Wall")
			self.rotatetask(90,-1,0)
			vel_msg.angular.z=0.0	
			rate= rospy.Rate(10)
			t0=rospy.Time.now().to_sec()
			current_dist=0
			while current_dist < yamlvalue:
				self.vel_publisher.publish(vel_msg)
				t1=rospy.Time.now().to_sec()
				current_dist=speed*(t1-t0)
				rate.sleep()
			self.rotatetask(90,-1,0)
			rotatecount = 1
			scanning = 1
		elif(count % 2 == 1):
			print("Wall")
			self.rotatetask(90,1,0)
			vel_msg.angular.z=0.0	
			rate= rospy.Rate(10)
			t0=rospy.Time.now().to_sec()
			current_dist=0
			while current_dist < yamlvalue:
				self.vel_publisher.publish(vel_msg)
				t1=rospy.Time.now().to_sec()
				current_dist=speed*(t1-t0)
				rate.sleep()
			self.rotatetask(90,1,0)
			rotatecount = 0
			scanning = 1
			
	
	def rotatetask(self,angle, clockwise, lspeed=0.0):
		
		if(clockwise == -1):			
			print("The robot turns clockwise with %s degree" % (angle))
		else:
			print("The robot turns counter clockwise with %s degree" % (angle))
			
		
		speed = 7			
		vel_msg =Twist()

		vel_msg.linear.x=0
		vel_msg.angular.z=0

		angularspeed = speed * (math.pi)/180
		vel_msg.angular.z=clockwise*abs(angularspeed)
		rate= rospy.Rate(10)
		t0=rospy.Time.now().to_sec()
		current_angle=0
		relativeangle = angle *(math.pi)/180
		while current_angle < relativeangle:
			self.vel_publisher.publish(vel_msg)
			t1=rospy.Time.now().to_sec()
			current_angle=angularspeed*(t1-t0)
			rate.sleep()
		vel_msg.linear.x=0
		vel_msg.angular.z=0
		self.vel_publisher.publish(vel_msg)	







if __name__ == "__main__":
	try:	
		robot_0 = Robot("0")
		robot_1 = Robot("1")
		global scanning
		global rotatecount
		r1 = rospy.get_param("R1")
		r2 = rospy.get_param("R2")
		print("robot_0 starts to moving")
		 
    		while True:		
			robot_0.movetask(scanning,rotatecount,r1)
			if(robot_0.get_position_x() > 6.0 and robot_0.get_position_x() < 8 and robot_0.get_position_y() > 1.5 and robot_0.get_position_y() < 3.5):
				time.sleep(0.5)
				break
				
 		print("robot_1 starts to moving")
		rotatecount = 1
		scanning = 1
		while True:		
			robot_1.movetask(scanning,rotatecount,r2)
			if(robot_1.get_position_x() > -1 and robot_1.get_position_x() < 1 and robot_1.get_position_y() > -4 and robot_1.get_position_y() < -2):
				time.sleep(0.5)
				break	
			

		
		print("End")


	except rospy.ROSInterruptException:
		pass


