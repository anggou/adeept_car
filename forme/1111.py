import time
import cv2
import RPi.GPIO as GPIO
import move
import servo

line_pin_right = 19
line_pin_middle = 16
line_pin_left = 20

global pwm0_direction, carState
try:
    carState = "stop"
    while True:
        status_right = GPIO.input(line_pin_right)
        status_middle = GPIO.input(line_pin_middle)
        status_left = GPIO.input(line_pin_left)
        keyValue = cv2.waitKey(1)
        if keyValue == ord('q'):
            break
        elif keyValue == 82:
            print("go")
            carState = "go"
        elif keyValue == 84:
            print("stop")
            carState = "stop"
        elif status_middle == 1 and status_left == 1 and status_right == 1:
            carState = "capture_stop"
            print("capture_stop")

        cap = cv2.VideoCapture(0)
        _, image = cap.read()
        image = cv2.flip(image, -1)
        cv2.imshow('pre', image)

        while carState == "go":
            try:
                print(11111111)
            except carState == "capture_stop":
                move.destroy()
                pass

        time.sleep(2)

        if carState == "stop":
            move.motorStop()
            break

    if carState == "stop":
        move.motorStop()

except KeyboardInterrupt:
    pass