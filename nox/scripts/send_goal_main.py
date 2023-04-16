#!/usr/bin/env python

import socket
import rospy
from std_msgs.msg import String
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

HOST = '0.0.0.0'
PORT = 5000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
print('Waiting for connections...')

conn, addr = s.accept()
print('Connected by ', addr)

def send_goal(x, y, w):
    rospy.init_node('send_goal_node')

    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = 'map'
    goal.target_pose.header.stamp = rospy.Time.now()

    goal.target_pose.pose.position.x = x
    goal.target_pose.pose.position.y = y
    goal.target_pose.pose.orientation.w = w

    client.send_goal(goal)
    client.wait_for_result()

    result = client.get_state()
    # rospy.loginfo("Goal sent. Result: %s", result)
    return result

while True:
    conn.sendall(b'start scan')
    data = conn.recv(1024)
    print('Received data:', data.decode())

    if data.decode() == 'done collecting':
        print('Start delivery')
        result = send_goal(-5.7, 2.8, 1.0)
        print(result)
        print('reach destination')
        conn.sendall(b'reach destination')
        break
