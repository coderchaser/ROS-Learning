#! /usr/bin/env python
# coding :utf-8

import rospy
import actionlib
from actionlib_msgs import *
from geometry_msgs.msg import Pose,Point,Quaternion,Twist
from move_base_msgs.msg import MoveBaseAction,MoveBaseGoal
from tf.transformations import quaternion_from_euler
from math import pi,radians

class Forward(object) :
	def __init__(self) :
		rospy.init_node('navigation_car_test',anonymous=True)

		rospy.on_shutdown(self.shutdown)

		quaternion_angle=Quaternion(*quaternion_from_euler(0,0,0,axes="sxyz"))
		length=rospy.get_param("~length",2.0)
		self.test_pose=Pose(Point(length,0.0,0.0),quaternion_angle)
		self.cmd_vel_pub=rospy.Publisher('cmd_vel',Twist)
		self.move_base=actionlib.SimpleActionClient("move_base",MoveBaseAction)

		rospy.loginfo("Waiting for the move_base server connected...")
		self.move_base.wait_for_server(rospy.Duration(30))

		rospy.loginfo("Connected to move_base server")
		rospy.loginfo("Starting test")

		
		self.goal=MoveBaseGoal()
		self.goal.target_pose.header.frame_id="map"
		self.goal.target_pose.header.stamp=rospy.Time.now()
		self.goal.target_pose.pose=self.test_pose
		self.move(self.goal)
	def move(self,goal) :
		self.move_base.send_goal(goal)
		finished_in_time=self.move_base.wait_for_result(rospy.Duration(30))

		if not finished_in_time :
			self.move_base.cancel_goal()
			rospy.loginfo("Time is out for arriving at the goal position :) ")
		else :
			statement=self.move_base.get_state()
			if statement == GoalStatus.SUCCEEDED :
				rospy.loginfo("Goal position arrived!")
	def shutdown(self) :
		rospy.loginfo("Stopping the car...")
		self.move_base.cancel_goal()
		rospy.sleep(2)
		self.cmd_vel_pub.publish(Twist())
		rospy.sleep(1)


if __name__ == '__main__':
	try:
		Forward()
	except rospy.ROSInterruptException :
		rospy.loginfo("Test Finished!")
