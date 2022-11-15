import move
import cv2
import RPi.GPIO as GPIO

cap = cv2.VideoCapture(0)

def capture_spare():
        keyValue = cv2.waitKey(0)
        i = 0
        filepath = "/home/pi/adeept_car/photos/train"
        _, image = cap.read()
        image = cv2.flip(image, -1)
        cv2.imshow('Capture_camera', image)
        height, _, _ = image.shape
        save_image = image[int(height / 2):, :, :]
        cv2.imshow('Save', save_image)
        if keyValue == ord('c'):
            cv2.imwrite("%s_%05d.png" % (filepath, 1), save_image)
        if keyValue == ord('q'):
            break


if __name__ == '__main__':
    capture_spare()
    cv2.destroyAllWindows()
    GPIO.cleanup()
