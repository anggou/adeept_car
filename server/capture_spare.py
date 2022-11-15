import move
import cv2
import RPi.GPIO as GPIO

cap = cv2.VideoCapture(0)

def capture_spare():
    i = 0
    while cap.isOpened():  # 초기화
        keyValue = cv2.waitKey(0)
        filepath = "/home/pi/adeept_car/photos/train"
        ret, image = cap.read()
        if not ret:
            break
        image = cv2.flip(image, -1)
        height, _, _ = image.shape
        save_image = image[int(height / 2):, :, :]
        cv2.imshow('Save', save_image)

        if keyValue == ord('q'):
            break
        if keyValue == 82:
          move.move(50, 'forward', 'no', 1)
          print("go")
        if keyValue == 84:
          move.motorStop()
          print("down")
        if keyValue == 81:
          move.move(50, 'forward', 'left', 0.6)
          print("left")
        if keyValue == 83:
          move.move(50, 'forward', 'right', 0.6)
          print("right")
        if keyValue == ord('1'):
          cv2.imwrite("%s_%05d_%03d.png" % (filepath, i, 1), save_image)
          i += 1
        if keyValue == ord('2'):
          cv2.imwrite("%s_%05d_%03d.png" % (filepath, i, 2), save_image)
          i += 1
        if keyValue == ord('3'):
          cv2.imwrite("%s_%05d_%03d.png" % (filepath, i, 3), save_image)
          i += 1
        if keyValue == ord('4'):
          cv2.imwrite("%s_%05d_%03d.png" % (filepath, i, 4), save_image)
          i += 1
        if keyValue == ord('5'):
          cv2.imwrite("%s_%05d_%03d.png" % (filepath, i, 5), save_image)
          i += 1
        if keyValue == ord('6'):
          cv2.imwrite("%s_%05d_%03d.png" % (filepath, i, 6), save_image)
          i += 1
        if keyValue == ord('0'):
            cv2.imwrite("%s_%05d_%03d.png" % (filepath, i, 0), save_image)
            i += 1


if __name__ == '__main__':
    capture_spare()
    cv2.destroyAllWindows()
    GPIO.cleanup()
