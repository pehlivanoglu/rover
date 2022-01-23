#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import matplotlib.pyplot as plt

motor_data = []
motor_data_time = []

def callback(data):
    global motor_data, motor_data_time

    motor_data = data.data.split(";")
    motor_data_time = data.header.stamp


def listener():
    rospy.init_node("motor_data_sub", anonymous=True)
    rospy.Subscriber("motor_data", String, callback)

    rospy.spin()

if __name__ == "__main__":
    listener()

    
    left_vel = motor_data[0]
    left_vol = motor_data[1]
    left_temp = motor_data[2]
    left_curr = motor_data[3]

    right_vel = motor_data[4]
    right_vol = motor_data[5]
    right_temp = motor_data[6]
    right_curr = motor_data[7]

    figure, axis = plt.subplots(2, 4)
  
    # Left Vel
    axis[0, 0].plot(motor_data_time, left_vel)
    axis[0, 0].set_title("Left vel")
    
    # Left Vol
    axis[0, 1].plot(motor_data_time, left_vol)
    axis[0, 1].set_title("Left vol")
    
    # For Tangent Function
    axis[0, 2].plot(motor_data_time, left_temp)
    axis[0, 2].set_title("Left temp")

    axis[0, 3].plot(motor_data_time, left_curr)
    axis[0, 3].set_title("Left curr")
    
    # For Tanh Function
    axis[1, 0].plot(motor_data_time, right_vel)
    axis[1, 0].set_title("Right vel")
    
    # Left Vol
    axis[1, 1].plot(motor_data_time, right_vol)
    axis[1, 1].set_title("Right vol")
    
    # For Tangent Function
    axis[1, 2].plot(motor_data_time, right_temp)
    axis[1, 2].set_title("Right temp")

    axis[1, 3].plot(motor_data_time, right_curr)
    axis[1, 3].set_title("Right curr")
    
    # Combine all the operations and display
    plt.show()