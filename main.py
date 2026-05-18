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


# Functions

def get_sign(num):
    if num < 0:
        return -1
    if num >= 0:
        return 1


# At start
ev3.speaker.set_volume(40); #ev3.speaker.beep(660,200)
ev3.speaker.beep(440)

# Declare Variables
BASE_SPEED = 700
target = 11 # light = ~24, black = 3
error = 0; last_error = 0; integral = 0; derivative = 0; correction = 0
kp = 10; ki = 0.2; kd = 1


# CODE BELOW

while True:
    value = center_sensor.reflection()
    error = (target - value) * kp
    integral = (integral + error) * ki
    derivative = (error - last_error) * kd
    last_error = error
    correction = error + integral + derivative
    print(value)
    print(error)
    print(integral)
    left_motor.run(BASE_SPEED + correction)
    right_motor.run(BASE_SPEED - correction)
    wait(3)

