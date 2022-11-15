import cv2

cap = cv2.VideoCapture(0)

def capture_spare():
        filepath = "/home/pi/adeept_car/photos/train"
        _, image = cap.read()
        image = cv2.flip(image, -1)
        height, _, _ = image.shape
        save_image = image[int(height / 2):, :, :]
        cv2.imwrite("%s_%05d.png" % (filepath, 1), save_image)

if __name__ == '__main__':
    capture_spare()
    cv2.destroyAllWindows()