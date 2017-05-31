#! /usr/bin/env python
# -*- coding:utf-8 -*-
# @author : Bob Liao
import rospy
from geometry_msgs.msg import Twist
from math import pi

class OutAndBack(object):
	def __init__(self) :
		rospy.init_node('out_and_back',anonymous=True)
		rospy.on_shutdown(self.shutdown)
		self.cmd_vel=rospy.Publisher('/cmd_vel',Twist)
		rate=20
		r=rospy.Rate(rate)
		linear_speed=0.15
		goal_distance=1.0
		linear_duration=goal_distance/linear_speed
		#angular_speed=1.0
		angular_speed=0.10
		goal_angle=pi
		angular_duration=goal_angle/angular_speed
		#print(angular_duration)
		for i in range(2) :
			move_cmd=Twist()
			move_cmd.linear.x=linear_speed
			ticks=int(linear_duration*rate)
			for t in range(ticks) :
				self.cmd_vel.publish(move_cmd)
				r.sleep()
			move_cmd =Twist()
			self.cmd_vel.publish(move_cmd)
			rospy.sleep(1)

			move_cmd.angular.z=angular_speed
			ticks=int(angular_duration*rate)
			for t in range(ticks) :
				self.cmd_vel.publish(move_cmd)
				r.sleep()
			move_cmd=Twist()
			self.cmd_vel.publish(move_cmd)
			rospy.sleep(1)
		self.cmd_vel.publish(Twist())
	def shutdown(self) :
		rospy.loginfo("Stopping the robot")
		self.cmd_vel.publish(Twist())
		rospy.sleep(1)

if __name__ == '__main__':
	try:
		OutAndBack()
	except rospy.ROSInterruptException :
		rospy.loginfo("Out-and-Back node terminated")
