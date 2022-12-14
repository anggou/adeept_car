import cv2
import tkinter 
from PIL import Image
from PIL import ImageTk
import findline
# import car_CV


def convert_to_tkimage():
    global src
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
    img = Image.fromarray(binary)
    imgtk = ImageTk.PhotoImage(image=img)
    label.config(image=imgtk)
    label.image = imgtk

window=tkinter.Tk()
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
label = tkinter.Label(window, image=imgtk)
label.pack(side="top")
button = tkinter.Button(window, text="find line", command=findline)
button.pack(side="bottom", expand=True, fill='both')
text = tkinter.Label(window,text='1111').grid(row=0)
window.mainloop()



