#!/usr/bin/env python
#coding:utf-8

import roslib
roslib.load_manifest('learning_tf')
import rospy
import math
import tf
import geometry_msgs.msg
import turtlesim.srv

if __name__ == '__main__':
	rospy.init_node('tf_turtle')

	listener=tf.TransformListener()
	rospy.wait_for_service('spawn')
	spawner=rospy.ServiceProxy('spawn',turtlesim.srv.Spawn)
	spawner(4,2,0,'turtle2')

	turtle_vel=rospy.Publisher('turtle2/cmd_vel',geometry_msgs.msg.Twist,queue_size=1)
	#Before, I make some mistakes here,and the two turtles will not follow the other,I fin
	#that i wrongly spell the 'turtle2/cmd/vel',that's the fault.I create another topic,but 
	#it does nothing.(No one subscribes it.)
	rate=rospy.Rate(10)
	#listener.waitForTransform("/turtle2","/turtle1",rospy.Time(),rospy.Duration(4.0))

	while not rospy.is_shutdown():
		try:
			now=rospy.Time.now()
			past=now-rospy.Duration(5.0)
			listener.waitForTransformFull("/turtle2",now,
										  "/turtle1",past,
										  "/world",rospy.Duration(1.0))
			#(trans,rot)=listener.lookupTransform('/turtle2','/carrot1',now)
			(trans,rot)=listener.lookupTransformFull("/turtle2",now,
													 "/turtle1",past,
													 "/world")
		except (tf.Exception,tf.LookupException,tf.ConnectivityException,tf.ExtrapolationException) :
			continue
		angular=4*math.atan2(trans[1],trans[0])
		linear=0.5*math.sqrt(trans[0]**2+trans[1]**2)
		cmd=geometry_msgs.msg.Twist()
		cmd.linear.x=linear
		cmd.angular.z=angular
		turtle_vel.publish(cmd)

		rate.sleep()