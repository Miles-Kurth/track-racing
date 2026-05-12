#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, GyroSensor, ColorSensor, TouchSensor
from pybricks.parameters import Port, Stop
from pybricks.tools import wait
from pybricks.robotics import DriveBase
from pybricks.iodevices import I2CDevice
from pybricks.parameters import Color
import time


# Initialize the EV3 Brick.
ev3 = EV3Brick()

# Initialize motors
left_motor = Motor(Port.B)
right_motor = Motor(Port.D)

# Initialize sensors
left_sensor = ColorSensor(Port.S4)
right_sensor = ColorSensor(Port.S1)

# Initialize drivebase
robot = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=104)

# Declare Variables
vel_reft = 0
vel_right = 0

# Functions

def left_check():
    if left_sensor.reflection() > 8:
        return False
    else:
        return True

def right_check():
    if right_sensor.reflection() > 8:
        return False
    else:
        return True


# At start
ev3.speaker.set_volume(40); #ev3.speaker.beep(660,200)
ev3.speaker.beep(440)


# CODE BELOW

vel_reft = 500
vel_right = 500

while True:
    # left_motor.run(vel_Left)
    # right_motor.run(vel_Right)
    if left_check():
        print(str(time.time()) + " " + str(left_sensor.reflection()))