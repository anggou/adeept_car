#!/usr/bin/python3
# File name   : findline.py
# Description : line tracking
# Website     : www.gewbot.com
# Author      : William
# Date        : 2019/08/28
import RPi.GPIO as GPIO
import move
import time
import servo

'''
status     = 1          #Motor rotation
forward    = 1          #Motor forward
backward   = 0          #Motor backward

left_spd   = num_import_int('E_M1:')         #Speed of the car
right_spd  = num_import_int('E_M2:')         #Speed of the car
left       = num_import_int('E_T1:')         #Motor Left
right      = num_import_int('E_T2:')         #Motor Right
'''

line_pin_right = 19
line_pin_middle = 16
line_pin_left = 20

'''
left_R = 15
left_G = 16
left_B = 18

right_R = 19
right_G = 21
right_B = 22

on  = GPIO.LOW
off = GPIO.HIGH

spd_ad_1 = 1
spd_ad_2 = 1
'''


def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(line_pin_right, GPIO.IN)
    GPIO.setup(line_pin_middle, GPIO.IN)
    GPIO.setup(line_pin_left, GPIO.IN)
    # motor.setup()


def T_L():
    status_right = GPIO.input(line_pin_right)
    status_middle = GPIO.input(line_pin_middle)
    status_left = GPIO.input(line_pin_left)
    # print('R%d   M%d   L%d'%(status_right,status_middle,status_left))
    if status_middle == 0 and status_left == 0 and status_right == 0:
        servo.ahead()
        move.move(25, 'forward', 'no', 1)
        print('LF3: %d   LF2: %d   LF1: %d\n' % (status_right, status_middle, status_left))
    elif status_middle == 1 and status_left == 1 and status_right == 1:
        print('LF3: %d   LF2: %d   LF1: %d\n' % (status_right, status_middle, status_left))
        move.motorStop()
    elif status_middle == 0 and status_left == 1 and status_right == 0:
        print('LF3: %d   LF2: %d   LF1: %d\n' % (status_right, status_middle, status_left))
        servo.lookright(100)
        move.move(20, 'forward', 'no', 0.6)
    elif status_middle == 0 and status_left == 0 and status_right == 1:
        print('LF3: %d   LF2: %d   LF1: %d\n' % (status_right, status_middle, status_left))
        servo.lookleft(100)
        move.move(20, 'forward', 'no', 0.6)
    else:
        print('LF3: %d   LF2: %d   LF1: %d\n' % (status_right, status_middle, status_left))
        move.move(30, 'backward', 'no', 1)
        time.sleep(1)


if __name__ == '__main__':
    try:
        # pwm0_direction = 1
        setup()
        move.setup()
        servo.servo_init()

        while 1:
            T_L()
        pass
    except KeyboardInterrupt:
        move.destroy()




