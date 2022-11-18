from __future__ import division
import time
# import Adafruit_PCA9685
# import ultra
import servo
# import move




if __name__ == '__main__':
        pwm0_direction = 1
        # move.motorStop()
        servo.lookleft(100)
        time.sleep(3)
        servo.lookright(100)
        # spare_capture()
        # time.sleep(1)
        servo.servo_init()
        # carState = "go"
