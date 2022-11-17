import cv2
def capture_spare():
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    filepath = "/home/pi/adeept_car/photos/train"
    i = 0


    while (cap.isOpened()):
        keyValue = cv2.waitKey(10)
        camera = "stop"
        if keyValue == ord('q'):
            break
        elif keyValue == ord('1'):
            print("1")
            camera = "1"
        elif keyValue == ord('2'):
            print("2")
            camera = "2"
        elif keyValue == ord('3'):
            print("3")
            camera = "3"
        elif keyValue == ord('4'):
            print("4")
            camera = "4"
        elif keyValue == ord('5'):
            print("5")
            camera = "5"
        elif keyValue == ord('6'):
            print("6")
            camera = "6"
        elif keyValue == ord('0'):
            print("0")
            camera = "0"


        _, image = cap.read()
        image = cv2.flip(image, -1)
        height, _, _ = image.shape
        save_image = image[int(height / 2):, :, :]
        save_image = cv2.resize(save_image, (200,66))
        cv2.imshow('Save', save_image)

        if camera == "1":
            cv2.imwrite("%s_%05d_%03d.png" % (filepath, i, 1), save_image)
            i += 1
        elif camera == "2":
            cv2.imwrite("%s_%05d_%03d.png" % (filepath, i, 2), save_image)
            i += 1
        elif camera == "3":
            cv2.imwrite("%s_%05d_%03d.png" % (filepath, i, 3), save_image)
            i += 1
        elif camera == "4":
            cv2.imwrite("%s_%05d_%03d.png" % (filepath, i, 4), save_image)
            i += 1
        elif camera == "5":
            cv2.imwrite("%s_%05d_%03d.png" % (filepath, i, 5), save_image)
            i += 1
        elif camera == "6":
            cv2.imwrite("%s_%05d_%03d.png" % (filepath, i, 6), save_image)
            i += 1
        elif camera == "0":
            cv2.imwrite("%s_%05d_%03d.png" % (filepath, i, 0), save_image)
            i += 1

        # cv2.destroyAllWindows()


if __name__ == '__main__':
    capture_spare()
    cv2.destroyAllWindows()