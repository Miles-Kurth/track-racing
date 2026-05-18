#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, GyroSensor, ColorSensor, TouchSensor
from pybricks.parameters import Port, Stop
from pybricks.tools import wait
from pybricks.robotics import DriveBase
from pybricks.iodevices import I2CDevice
from pybricks.parameters import Color
import time
import math


# Initialize the EV3 Brick.
ev3 = EV3Brick()

# Initialize motors
left_motor = Motor(Port.B)
right_motor = Motor(Port.D)

# Initialize sensors
left_sensor = ColorSensor(Port.S1)
right_sensor = ColorSensor(Port.S4)
center_sensor = ColorSensor(Port.S3)

# Initialize drivebase
robot = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=104)

# Declare Variables
vel_left = 0
vel_right = 0
START_SPEED = 300
last_side = "between" # left, right


# Functions

def get_sign(num):
    if num < 0:
        return -1
    if num >= 0:
        return 1

def update_motors():
    update_left()
    update_right()

def update_left():
    global vel_left; global START_SPEED
    left_motor.run(START_SPEED + vel_left)

def update_right():
    global vel_right; global START_SPEED
    right_motor.run(START_SPEED + vel_right)


def left_check():
    global last_side
    if left_sensor.reflection() > 8:
        return False
    else:
        last_side = "left"
        return True

def right_check():
    global last_side
    if right_sensor.reflection() > 8:
        return False
    else:
        last_side = "right"
        return True

def center_check():
    if center_sensor.reflection() > 8:
        return False
    else:
        return True

def fix_deviation():
    global vel_left; global vel_right; global last_side

    if not (left_check() or right_check() or center_check()): # off the track
        vel_left *= 1.1; vel_right *= 1.1
    
    if center_check():
        vel_left *= 0.8; vel_right *= 0.8

def fix_vels():
    global vel_left; global vel_right

    vel_left = round(vel_left); vel_right = round(vel_right)
    if abs(vel_left) > 100:
        vel_left = 100 * get_sign(vel_left)
    if abs(vel_right) > 100:
        vel_right = 100 * get_sign(vel_right)

    total = vel_left + vel_right
    difference = abs(vel_left - vel_right)

    if not (left_check() or right_check()) and center_check(): # directly on line
        vel_left = 0; vel_right = 0
        
    
    # bring closer to straight
    # if difference <= 200:
        
    




# At start
ev3.speaker.set_volume(40); #ev3.speaker.beep(660,200)
ev3.speaker.beep(440)


# CODE BELOW

vel_left = 0
vel_right = 0



update_motors()
while True:
    if left_check(): # turn left
        vel_right += 1
        vel_left += -1
        fix_vels()
        update_motors()
    
    if right_check(): # turn right
        vel_left += 1
        vel_right += -1
        fix_vels()
        update_motors()
    fix_deviation()


    # print info
    print("Total = " + str(vel_left + vel_right) + ",   ", end="") # total speed
    print("L = " + str(vel_left) + str(left_check()) + "  ", end="") # LEFT speed & [sees line?]
    print("R = " + str(vel_right) + str(right_check())) # RIGHT speed & [sees line?]

# do PID