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
left_sensor = ColorSensor(Port.S4)
right_sensor = ColorSensor(Port.S1)
center_sensor = ColorSensor(Port.S3)

# Initialize drivebase
robot = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=104)

# Declare Variables
vel_left = 0
vel_right = 0
MAX_TOTAL = 1000
last_side = "between" # left, right


# Functions

def update_motors():
    update_left()
    update_right()

def update_left():
    global vel_left
    left_motor.run(vel_left)

def update_right():
    global vel_right
    right_motor.run(vel_right)


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
        if last_side == "left": # turning left
            vel_right = 600; vel_left = 400
        if last_side == "right": #turning right
            vel_left = 600; vel_right = 400

def fix_vels():
    global vel_left; global vel_right

    vel_left = round(vel_left); vel_right = round(vel_right)
    total = vel_left + vel_right

    
    difference = abs(vel_left - vel_right)

    if not (left_check() or right_check()) and center_check(): # directly on line
        vel_left = 500; vel_right = 500

    # bring closer to straight
    if center_check():
        difference *= 1.5
    if difference > 200:
        if vel_left > vel_right:
            vel_left -= (difference / 5); vel_right += (difference / 5)
        if vel_right > vel_left:
            vel_right -= (difference / 5); vel_left += (difference / 5)
    




# At start
ev3.speaker.set_volume(40); #ev3.speaker.beep(660,200)
ev3.speaker.beep(440)


# CODE BELOW

vel_left = 300
vel_right = 300

update_motors()
while True:
    if left_check():
        vel_right += -1
        vel_left -= -1
        fix_vels()
        update_motors()
    if right_check():
        vel_left += -1
        vel_right -= -1
        fix_vels()
        update_motors()
    fix_deviation()

    print("Total = " + str(vel_left + vel_right) + ",  ", end="")
    print("L = " + str(vel_left) + str(left_check()) + "  ", end="")
    print("R = " + str(vel_right) + str(right_check()))
    