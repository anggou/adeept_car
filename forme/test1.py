import time
import cv2
from tensorflow.keras.models import load_model


cap = cv2.VideoCapture(-1)
if cap.isOpened():
    
    while True:
        ret, image = cap.read()
        if ret:
            cv2.imshow('camera', image)
            if cv2.waitKey(1)!=-1:
                break
else:
    print("cc")
        
cap.release()
cv2.destroyAllWindows()
