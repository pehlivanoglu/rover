#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rospy
import matplotlib.pyplot as plt
from std_msgs.msg import String
import time
import matplotlib as mpl


motor_dataL = {"velocity":[0],"voltage":[0],"temperature":[0],"current":[0]}

motor_dataR= {"velocity":[0],"voltage":[0],"temperature":[0],"current":[0]}

def plotting(data):
    global fig, ax
    data_list = data.data.split(";")
    
    motor_dataL["velocity"].append(float(data_list[0]))
    motor_dataL["voltage"].append(float(data_list[1]))
    motor_dataL["temperature"].append(float(data_list[2]))
    motor_dataL["current"].append(float(data_list[3]))
    motor_dataR["velocity"].append(float(data_list[4]))
    motor_dataR["voltage"].append(float(data_list[5]))
    motor_dataR["temperature"].append(float(data_list[6]))
    motor_dataR["current"].append(float(data_list[7]))
    #plt.ion()
    #fig, ax = plt.subplots(2,2)

    if len(motor_dataL["velocity"]) <20:
        #fig, ax = plt.subplots(2,2)
        ax[0,0].plot(motor_dataL["velocity"],color = "red",label = "left(m/s)")
        ax[0,0].plot(motor_dataR["velocity"],color = "blue",label = "rigth(m/s)")
        ax[0,0].set_title("Velocity (m/s)")



        ax[0,1].plot(motor_dataL["voltage"],color = "red")
        ax[0,1].plot(motor_dataR["voltage"],color = "blue")
        ax[0,1].set_title("Voltage (Volts)")

        ax[1,0].plot(motor_dataL["temperature"],color = "red")
        ax[1,0].plot(motor_dataR["temperature"],color = "blue")
        ax[1,0].set_title("Temperature (C)")

        ax[1,1].plot(motor_dataL["current"],color = "red")
        ax[1,1].plot(motor_dataR["current"],color = "blue")
        ax[1,1].set_title("Current (Amperes)")

        fig.canvas.draw()
        fig.canvas.flush_events()
        time.sleep(0.001)

    else:
        ax[0,0].plot(motor_dataL["velocity"][-20:],color = "red",label = "left(m/s)")
        ax[0,0].plot(motor_dataR["velocity"][-20:],color = "blue")
        ax[0,0].set_title("Velocity (m/s)")


        ax[0,1].plot(motor_dataL["voltage"][-20:],color = "red")
        ax[0,1].plot(motor_dataR["voltage"][-20:],color = "blue")
        ax[0,1].set_title("Voltage (Volts)")

        ax[1,0].plot(motor_dataL["temperature"][-20:],color = "red")
        ax[1,0].plot(motor_dataR["temperature"][-20:],color = "blue")
        ax[1,0].set_title("Temperature (C)")

        ax[1,1].plot(motor_dataL["current"][-20:],color = "red")
        ax[1,1].plot(motor_dataR["current"][-20:],color = "blue")
        ax[1,1].set_title("Current (Amperes)")

        fig.canvas.draw()
        fig.canvas.flush_events()
        ax[0,0].cla()
        ax[0,1].cla()         
        ax[1,0].cla()  
        ax[1,1].cla()
        time.sleep(0.001)
    



if __name__ == '__main__' :

    rospy.init_node('graph' , anonymous=True)
    plt.ion()
    fig, ax = plt.subplots(2,2)
    fig.suptitle('Red -> Left Track | Blue -> Right Track', fontsize=15)
    rospy.Subscriber('chatter', String , plotting)
    
     
    rospy.spin()
