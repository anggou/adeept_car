import time
import cv2
import RPi.GPIO as GPIO
import numpy as np
from tensorflow.keras.models import load_model
import move
import servo

line_pin_right = 19
line_pin_middle = 16
line_pin_left = 20

cap = cv2.VideoCapture(0)
spare = "None"
result = []
carState = "stop"

def img_preprocess(image):
    height, _, _ = image.shape
    image = image[int(height / 2):, :, :]
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
    image = cv2.resize(image, (200, 66))
    # image = cv2.GaussianBlur(image, (5, 5), 0)
    _, image = cv2.threshold(image, 160, 255, cv2.THRESH_BINARY_INV) #확인확인
    image = image / 255
    return image

def spare_capture():
    model_spare = load_model('/home/pi/adeept_car/model/spare_model.h5')
    global spare, result
    # model 설정

    try:
        spare = "None"
        classes = ['Empty', 'Spindle_1', 'Spindle_2', 'Spindle_3', 'Spring_1', 'Spring_2', 'Spring_3']
        _, image = cap.read()
        image = cv2.flip(image, 1)
        preprocessed = img_preprocess(image)
        cv2.imshow('pre', preprocessed)
        X = np.asarray([preprocessed])
        idx = int(model.predict(X)[0])
        print("idx :", idx)
        spare = int(classes[idx])

        print("spare is:", spare)
        if spare == 'Empty':
            print("Empty")  # GUI로 보내기
            result.append('Empty')
        elif spare == 'Spindle_1':
            print("Spindle_1")  # GUI로 보내기
            result.append('Spindle_1')
        elif spare == 'Spindle_2':
            print("Spindle_2")  # GUI로 보내기
            result.append('Spindle_2')
        elif spare == 'Spindle_3':
            print("Spindle_3")  # GUI로 보내기
            result.append('Spindle_3')
        elif spare == 'Spring_1':
            print("Spring_1")  # GUI로 보내기
            result.append('Spring_1')
        elif spare == 'Spring_2':
            print("Spring_2")  # GUI로 보내기
            result.append('Spring_2')
        elif spare == 'Spring_3':
            print("Spring_3")  # GUI로 보내기
            result.append('Spring_3')

    except KeyboardInterrupt:
        pass

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
    if status_middle == 0 and status_left == 0 and status_right == 0:
        servo.ahead()
        move.move(25, 'forward', 'no', 1)
        print('LF3: %d   LF2: %d   LF1: %d\n' % (status_right, status_middle, status_left))
    elif status_middle == 1 and status_left == 1 and status_right == 1:
        print('LF3: %d   LF2: %d   LF1: %d\n' % (status_right, status_middle, status_left))
        move.motorStop()
    elif status_middle == 0 and status_left == 1 and status_right == 0:
        print('LF3: %d   LF2: %d   LF1: %d\n' % (status_right, status_middle, status_left))
        servo.lookright(10)
        move.move(25, 'forward', 'no', 0.6)
    elif status_middle == 0 and status_left == 0 and status_right == 1:
        print('LF3: %d   LF2: %d   LF1: %d\n' % (status_right, status_middle, status_left))
        servo.lookleft(10)
        move.move(25, 'forward', 'no', 0.6)
    else:
        print('LF3: %d   LF2: %d   LF1: %d\n' % (status_right, status_middle, status_left))
        move.move(30, 'backward', 'no', 1)
        time.sleep(1)


def main():
    check_spare = '/home/pi/adeept_car/model/checkspare_final.h5'
    model = load_model(check_spare)
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

            _, image = cap.read()
            image = cv2.flip(image, -1)
            preprocessed = img_preprocess(image)
            cv2.imshow('pre', preprocessed)

            X = np.asarray([preprocessed])
            steering_angle = int(model.predict(X)[0])
            print("predict angle:", steering_angle)

            while True:
                if carState == "go":
                    try:
                        setup()
                        move.setup()
                        while 1:
                            pwm0_direction = 1
                            T_L()
                        pass
                    except KeyboardInterrupt:
                        move.destroy()
                if carState == "capture_stop":
                    move.motorStop()
                    servo.up(180)
                    time.sleep(3)
                    spare_capture()
                    time.sleep(1)
                    servo.down(180)
                    time.sleep(1)
                    continue
                if carState == "stop":
                    move.motorStop()
                    break

        if carState == "stop":
            move.motorStop()
            ##### 여기서 다시 carstate = go 로 반환하는구문 추가

    except KeyboardInterrupt:
        pass

    # main()
    # cv2.destroyAllWindows()

if __name__ == '__main__':
    try:
        setup()
        move.setup()
        main()
    except KeyboardInterrupt:
        move.destroy()
        cv2.destroyAllWindows()
