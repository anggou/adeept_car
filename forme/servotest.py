import time
import RPi.GPIO as GPIO
import numpy as np
import move
import servo



if __name__ == '__main__':
    move.setup()
    servo.up(180)
    time.sleep(2)
    servo.down(180)
