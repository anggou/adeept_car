import cv2
from tkinter import *
from PIL import Image
from PIL import ImageTk

path ="/home/pi/adeept_car/photos/train_00000_001.png"
window=Tk()
window.title("Space Stock")
window.geometry("640x300")

def readtoimg(image):
    src = cv2.flip(image, 1)
    src = cv2.resize(src, (210, 150))
    img = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    img = ImageTk.PhotoImage(image=img)
    return img
    

image = cv2.imread("/home/pi/adeept_car/photos/train_00000_001.png",1)
imgtk1 = readtoimg(image)

image = cv2.imread("/home/pi/adeept_car/photos/train_00001_002.png",1)
imgtk2 = readtoimg(image)

image = cv2.imread("/home/pi/adeept_car/photos/train_00002_003.png",1)
imgtk3 = readtoimg(image)


label1 = Label(window, image=imgtk1)
label2 = Label(window, image=imgtk2)
label3 = Label(window, image=imgtk3)
label1.pack(side="left")
label2.pack(side="left")
label3.pack(side="left")


spare1 = Label(window, text='1111111111')
spare1.place(x=20,y=250)

spare2 = Label(window, text='2222')
spare2.place(x=20+210,y=250)

spare3 = Label(window, text='3333')
spare3.place(x=20+420,y=250)

text = Text(window, width = 1 , height= 1)
text.pack(side="bottom")

button = Button(window, text="Spare_results", command=convert_to_tkimage)
button.pack(side="bottom", expand=True, fill='both')
window.mainloop()

