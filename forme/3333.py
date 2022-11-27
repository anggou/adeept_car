import time
import cv2
import RPi.GPIO as GPIO
import move
import servo
from tensorflow.keras.models import load_model
import numpy as np
from tkinter import *
from PIL import Image
from PIL import ImageTk

line_pin_right = 19
line_pin_middle = 16
line_pin_left = 20
carState = "none"
cap = cv2.VideoCapture(0)
result = []
spare = "none"
servo.servo_init()
i = 0
path = "/home/pi/adeept_car/photos/spare"
classes = ['Empty', 'Spindle_1', 'Spindle_2', 'Spindle_3', 'Spring_1', 'Spring_2', 'Spring_3']
model = load_model('/home/pi/adeept_car/forme/keras_model.h5')
spare_number = 3


def spare_capture():
    global spare, cap, result, i, classes, model

    size = (224, 224)
    ret, img = cap.read()
    h, w, _ = img.shape
    cx = h / 2
    img = img[:, 200:200 + img.shape[0]]
    img = cv2.flip(img, 1)
    cv2.imwrite("%s_%05d.png" % (path, i), img)
    i += 1
    img_input = cv2.resize(img, size)
    img_input = cv2.cvtColor(img_input, cv2.COLOR_BGR2RGB)
    img_input = (img_input.astype(np.float32) / 127.0) - 1
    img_input = np.expand_dims(img_input, axis=0)
    prediction = model.predict(img_input)
    idx = np.argmax(prediction)
    spare = classes[idx]
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


def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(line_pin_right, GPIO.IN)
    GPIO.setup(line_pin_middle, GPIO.IN)
    GPIO.setup(line_pin_left, GPIO.IN)
    # motor.setup()


def just_go(sec):
    move.move(25, 'forward', 'no', 1)
    time.sleep(sec)


def Tracking_line():
    if status_middle == 0 and status_left == 0 and status_right == 0:
        servo.ahead()
        move.move(25, 'forward', 'no', 1)
        print('LF3: %d   LF2: %d   LF1: %d\n' % (status_right, status_middle, status_left))
    # elif status_middle == 0 and status_left == 1 and status_right == 0:
    elif status_middle == 1:
        print('LF3: %d   LF2: %d   LF1: %d\n' % (status_right, status_middle, status_left))
        move.motorStop()
    elif status_left == 1:
        # elif status_middle == 0 and status_left == 1 and status_right == 0:
        print('LF3: %d   LF2: %d   LF1: %d\n' % (status_right, status_middle, status_left))
        servo.lookright(10)
        move.move(25, 'forward', 'no', 0.6)
    elif status_right == 1:
        print('LF3: %d   LF2: %d   LF1: %d\n' % (status_right, status_middle, status_left))
        servo.lookleft(10)
        move.move(25, 'forward', 'no', 0.6)
    else:
        print('LF3: %d   LF2: %d   LF1: %d\n' % (status_right, status_middle, status_left))
        move.move(30, 'backward', 'no', 1)
        time.sleep(1)


def readtoimg(image):
    src = cv2.flip(image, 1)
    src = cv2.resize(src, (210, 150))
    img = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    img = ImageTk.PhotoImage(image=img)
    return img


def show_gui(number):
    global result
    window = Tk()
    window.title("Space Stock")
    window.geometry("640x300")
    file = "/home/pi/adeept_car/photos/spare"

    for i in range(number):
        image = cv2.imread("%s_%05d.png" % (file, i), 1)
        globals()["image{}".format(i)] = readtoimg(image)
        globals()["label{}".format(i)] = Label(window, image=globals()["image{}".format(i)])
        globals()["label{}".format(i)].pack(side="left")

    spare1 = Label(window, text='1111111111')
    spare1.place(x=20, y=250)

    spare2 = Label(window, text='2222')
    spare2.place(x=20 + 210, y=250)

    spare3 = Label(window, text='3333')
    spare3.place(x=20 + 420, y=250)

    text = Text(window, width=1, height=1)
    text.pack(side="bottom")

    window.mainloop()


try:
    global result
    while True:
        setup()
        move.setup()
        keyValue = cv2.waitKey(1)
        _, image = cap.read()
        image = cv2.flip(image, -1)
        cv2.imshow('pre', image)

        status_right = GPIO.input(line_pin_right)
        status_middle = GPIO.input(line_pin_middle)
        status_left = GPIO.input(line_pin_left)

        if keyValue == ord('q'):
            break
        elif keyValue == 82:
            print("go")
            carState = "go"
        elif keyValue == 84:
            print("stop")
            carState = "stop"
        elif carState == "all_stop":
            servo.servo_init()
            servo.lookdown(100)
            show_gui(len(result))

        elif carState == "stop":
            time.sleep(3)
            move.motorStop()

        while carState == "go":
            status_right = GPIO.input(line_pin_right)
            status_middle = GPIO.input(line_pin_middle)
            status_left = GPIO.input(line_pin_left)
            setup()
            Tracking_line()

            if status_middle == 1 and status_left == 1 and status_right == 1:
                move.motorStop()
                servo.up(180)
                time.sleep(4)
                spare_capture()
                servo.down(180)
                print("capture")
                print(result)
                just_go(1)

            if len(result) == spare_number:
                move.motorStop()
                print(len(result))
                carState = "all_stop"

                break

except KeyboardInterrupt:
    pass
