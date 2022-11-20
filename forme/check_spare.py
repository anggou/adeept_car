import tensorflow.keras
import numpy as np
import cv2

model = tensorflow.keras.models.load_model('../model/keras_model.h5')  # file 집어넣기
cap = cv2.VideoCapture(0)
size = (224, 224)
classes = ['Empty', 'Spindle_1', 'Spindle_2', 'Spindle_3', 'Spring_1', 'Spring_2', 'Spring_3']

def img_preprocess(image):
    height, _, _ = image.shape
    image = image[int(height/2):,:,:]
    image = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
    image = cv2.GaussianBlur(image, (3,3), 0)
    image = cv2.resize(image, (200,66))
    image = image / 255
    return image


def spare_capture():
    camera = cv2.VideoCapture(-1)
    camera.set(3, 640)
    camera.set(4, 480)
    model_path = '/home/pi/adeept_car/model/spare_model.h5'
    model = load_model(model_path)
    # model 설정

    while (camera.isOpened()):

        keValue = cv2.waitKey(1)
        if keValue == ord('q'):
            print("capture")
        _, image = camera.read()
        image = cv2.flip(image, -1)
        cv2.imshow('Original', image)

        preprocessed = img_preprocess(image)
        cv2.imshow('pre', preprocessed)

        X = np.asarray([preprocessed])
        idx = int(model.predict(X)[0])
        spare = int(classes[idx])
        print("spare is:", spare)
        if spare == 'Empty':
            print("Empty")  # GUI로 보내기
        elif spare == 'Spindle_1':
            print("Spindle_1")  # GUI로 보내기
        elif spare == 'Spindle_2':
            print("Spindle_2")  # GUI로 보내기
        elif spare == 'Spindle_3':
            print("Spindle_3")  # GUI로 보내기
        elif spare == 'Spring_1':
            print("Spring_1")  # GUI로 보내기
        elif spare == 'Spring_2':
            print("Spring_2")  # GUI로 보내기
        elif spare == 'Spring_3':
            print("Spring_3")  # GUI로 보내기

        if keValue == ord('q'):
            break
    cv2.destroyAllWindows()


if __name__ == '__main__':
    spare_capture()
    cv2.destroyAllWindows()
