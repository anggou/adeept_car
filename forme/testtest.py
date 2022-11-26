from tensorflow.keras.models import load_model
import numpy as np
import cv2
import tensorflow as tf
from tkinter import *
from PIL import Image
from PIL import ImageTk
import os

model = load_model('keras_model.h5')
# model = load_model('/home/pi/adeept_car/forme/keras_model.h5')
cap = cv2.VideoCapture(0)
size = (224, 224)
classes = ['Empty', 'Spindle_1', 'Spindle_2', 'Spindle_3', 'Spring_1', 'Spring_2', 'Spring_3']
result = []

window = Tk()
window.title("spares")
window.geometry("640x480+100+100")


while cap.isOpened():
    ret, img = cap.read()
    if not ret:
        break

    h, w, _ = img.shape
    cx = h / 2
    img = img[:, 200:200 + img.shape[0]]
    img = cv2.flip(img, 1)

    img_input4 = cv2.resize(img, size)
    img_input4_1 = cv2.cvtColor(img_input4, cv2.COLOR_BGR2RGB)
    img_input4_2 = Image.fromarray(img_input4_1)
    imgtk = ImageTk.PhotoImage(image=img_input4_2)

    img_input3 = cv2.cvtColor(img_input4, cv2.COLOR_BGR2RGB)
    img_input2 = (img_input3.astype(np.float32) / 127.0) - 1
    img_input = np.expand_dims(img_input2, axis=0)

    prediction = model.predict(img_input)
    idx = np.argmax(prediction)

    # cv2.putText(img, text=classes[idx], org=(10, 30), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.8, color=(255, 255, 255), thickness=2)

    if classes[idx] == 'Empty':
        print("Empty")  # GUI로 보내기
        result.append('Empty')
    elif classes[idx] == 'Spindle_1':
        print("Spindle_1")  # GUI로 보내기
        result.append('Spindle_1')
    elif classes[idx] == 'Spindle_2':
        print("Spindle_2")  # GUI로 보내기
        result.append('Spindle_2')
    elif classes[idx] == 'Spindle_3':
        print("Spindle_3")  # GUI로 보내기
        result.append('Spindle_3')
    elif classes[idx] == 'Spring_1':
        print("Spring_1")  # GUI로 보내기
        result.append('Spring_1')
    elif classes[idx] == 'Spring_2':
        print("Spring_2")  # GUI로 보내기
        result.append('Spring_2')
    elif classes[idx] == 'Spring_3':
        print("Spring_3")  # GUI로 보내기
        result.append('Spring_3')

    img_gui = Label(window, image=imgtk)
    img_gui.pack(side="top")
    spare = Label(window, text=result)
    spare.place(x=10, y=10)
    window.mainloop()
    # cv2.imshow('result', img)
    if cv2.waitKey(1) == ord('q'):
        break
