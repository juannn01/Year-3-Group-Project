#!/usr/bin/env python

import socket
#import rospy
#from std_msgs.msg import String
#import actionlib
#from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

HOST = '0.0.0.0'
PORT = 5000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
print('Waiting for connections...')

conn, addr = s.accept()
print('Connected by ', addr)

conn.sendall(b'start scan')
data = conn.recv(1024)
print("Received data:", data.decode())
