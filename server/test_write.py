import cv2

cap = cv2.VideoCapture(0)


def capture_spare():
    i = 0
    while cap.isOpened():  # 초기화
        keyValue = cv2.waitKey(0)
        filepath = "/home/pi/adeept_car/photos/train"
        _, image = cap.read()
        image = cv2.flip(image, -1)
        height, _, _ = image.shape
        save_image = image[int(height / 2):, :, :]
        cv2.imshow('Save', save_image)
        if keyValue == ord('c'):
            cv2.imwrite("%s_%05d_%03d.png" % (filepath, i, 1), save_image)
            i += 1
        if keyValue == ord('q'):
            break


if __name__ == '__main__':
    capture_spare()
    cv2.destroyAllWindows()
