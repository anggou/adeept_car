import time
import RPi.GPIO as GPIO
import numpy as np
import move
import servo



if __name__ == '__main__':
    servo.servo_init()
    move.setup()
    servo.lookup(50)
    time.sleep(2)
    servo.lookdown(50)
