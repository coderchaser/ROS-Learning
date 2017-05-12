#!/usr/bin/env python
# -*- coding:utf-8 -*-

import rospy
from geometry_msgs.msg import Twist,Point,Quaternion
import tf
from rbx1_nav.transform_utils import quat_to_angle,normalize_angle
from math import radians,copysign,sqrt,pow,pi

class OutAndBack() :
	def __init__(self) :
		rospy.init_node('out_and_back',anonymous=True)

		rospy.on_shutdown(self.shutdown)
		self.cmd_vel=rospy.Publisher('/cmd_vel',Twist)
		rate=20
		r=rospy.Rate(rate)
		linear_speed=0.2
		goal_distance=1.0
		angular_speed=1.0
		angular_tolerance=radians(2.5)
		goal_angle=pi
		self.tf_listener=tf.TransformListener()
		rospy.sleep(2)
		self.odom_frame='/odom'
		try :
			self.tf_listener.waitForTransform(self.odom_frame,'/base_footprint',rospy.Time(),rospy.Duration(1,0))
			self.base_frame='/base_footprint'
			print(self.base_frame)
		except(tf.Exception,tf.ConnectivityException,tf.LookupException) :
			try :
				self.tf_listener.waitForTransform (self.odom_frame,'/base_link',rospy.Time(),rospy.Duration(1.0))
				self.base_frame='/base_link'
			except (tf.Exception,tf.ConnectivityException,tf.LookupException) :
				rospy.loginfo('Cannot find transform between /odom and /base_link or /base_footprint')
				rospy.signal_shutdown('tf Exception')
		position=Point()
		for i in range(2) :
			move_cmd=Twist()
			move_cmd.linear.x=linear_speed
			(position,rotation)=self.get_odom()
			x_start=position.x
			y_start=position.y
			distance=0
			while distance<goal_distance and not rospy.is_shutdown() :
				self.cmd_vel.publish(move_cmd)

				r.sleep()
				(position,rotation)=self.get_odom()
				distance=sqrt(pow((position.x-x_start),2)+pow((position.x-y_start), 2))
			move_cmd=Twist()
			self.cmd_vel.publish(move_cmd)
			rospy.sleep(1)
			move_cmd.angular.z=angular_speed
			last_angle=rotation
			turn_angle=0
			while abs(turn_angle+angular_tolerance) < abs(goal_angle) and not rospy.is_shutdown():
				self.cmd_vel.publish(move_cmd)
				r.sleep()
				(position,rotation)=self.get_odom()
				delta_angle=normalize_angle(rotation-last_angle)
				turn_angle+=delta_angle
				last_angle=rotation
			move_cmd=Twist()
			self.cmd_vel.publish(move_cmd)
			rospy.sleep(1)
		self.cmd_vel.publish(Twist())
	def get_odom(self) :
		try :
			(trans,rot) =self.tf_listener.lookupTransform(self.odom_frame,self.base_frame,rospy.Time(0))
		except (tf.Exception,tf.ConnectivityException,tf.LookupException) :
			rospy.loginfo('TF Exception')
			return
		return (Point(*trans),quat_to_angle(Quaternion(*rot)))
	def shutdown(self) :
		rospy.loginfo('Stopping the robot...')
		self.cmd_vel.publish(Twist())
		rospy.sleep(1)


if __name__ == '__main__':
	try:
		OutAndBack()
		print('Hello')
	except :
		rospy.loginfo('Out-and-Back node terminated.')