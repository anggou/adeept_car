import cv2
from tkinter import *
from PIL import Image
from PIL import ImageTk


def convert_to_tkimage():
    global src
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
    img = Image.fromarray(binary)
    imgtk = ImageTk.PhotoImage(image=img)
    label.config(image=imgtk)
    label.image = imgtk

window=Tk()
window.title("YUN DAE HEE")
window.geometry("640x480+100+100")

cap = cv2.VideoCapture(0)
_, image = cap.read()
src = cv2.flip(image, 1)
# src = cv2.imread("giraffe.jpg")
src = cv2.resize(src, (640, 400))
img = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)

img = Image.fromarray(img)
imgtk = ImageTk.PhotoImage(image=img)
# 사진 찍는걸로 추정
label = Label(window, image=imgtk)
label.pack(side="top")

spare = Label(window, text='1111111111')
spare.place(x=10,y=10)

text = Text(window, width = 1 , height= 1)
text.pack(side="bottom")

button = Button(window, text="Spare_results", command=convert_to_tkimage)
button.pack(side="bottom", expand=True, fill='both')
window.mainloop()

