#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist

if __name__ == '__main__':
	rospy.init_node('test_topic',anonymous=True)
	rospy.loginfo('Start to send messages to /bob')
	p=rospy.Publisher('/bob',Twist)
	msg=Twist()
	msg.linear.x=20
	msg.angular.z=0.5
	r=rospy.Rate(0.5)
	i=10
	while i :
		p.publish(msg)
		r.sleep()
		i-=1
		print(i)
	rospy.loginfo('Stop the message')
	p.publish(Twist())