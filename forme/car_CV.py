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
pwm0_direction = '1'


def img_preprocess(image):
    height, _, _ = image.shape
    image = image[int(height / 2):, :, :]
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
    image = cv2.resize(image, (200, 66))
    # image = cv2.GaussianBlur(image, (5, 5), 0)
    _, image = cv2.threshold(image, 160, 255, cv2.THRESH_BINARY_INV)  # 확인확인
    image = image / 255
    return image


def spare_capture():
    global spare, cap
    model = load_model('/home/pi/adeept_car/forme/keras_model.h5')
    size = (224, 224)
    classes = ['Empty', 'Spindle_1', 'Spindle_2', 'Spindle_3', 'Spring_1', 'Spring_2', 'Spring_3']

    while cap.isOpened():
        ret, img = cap.read()
        if not ret:
            break

        h, w, _ = img.shape
        cx = h / 2
        img = img[:, 200:200 + img.shape[0]]
        img = cv2.flip(img, 1)
        cv2.imshow('result', img)

        img_input = cv2.resize(img, size)
        img_input = cv2.cvtColor(img_input, cv2.COLOR_BGR2RGB)
        img_input = (img_input.astype(np.float32) / 127.0) - 1
        img_input = np.expand_dims(img_input, axis=0)

        prediction = model.predict(img_input)
        idx = np.argmax(prediction)
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

        # cv2.putText(img, text=classes[idx], org=(10, 30), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.8, color=(255, 255, 255), thickness=2)

        if cv2.waitKey(1) == ord('q'):
            break


def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(line_pin_right, GPIO.IN)
    GPIO.setup(line_pin_middle, GPIO.IN)
    GPIO.setup(line_pin_left, GPIO.IN)
    # motor.setup()


def Tracking_line():
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

            while carState == "go":
                try:
                    setup()
                    move.setup()
                    Tracking_line()
                except carState == "capture_stop":
                    move.destroy()
                    pass

            if carState == "stop":
                move.motorStop()
                break

        if carState == "stop":
            move.motorStop()

    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    try:
        setup()
        move.setup()
        main()
    except KeyboardInterrupt:
        move.destroy()
        cv2.destroyAllWindows()