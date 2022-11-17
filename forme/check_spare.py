import tensorflow.keras
import numpy as np
import cv2

model = tensorflow.keras.models.load_model('../model/keras_model.h5')  # file 집어넣기
cap = cv2.VideoCapture(0)
size = (224, 224)
classes = ['Empty', 'Spindle_1', 'Spindle_2', 'Spindle_3', 'Spring_1', 'Spring_2', 'Spring_3']


def spare_capture():
    model_spare = load_model('/home/pi/adeept_car/model/spare_model.h5')
    global spare, img_input
    # model 설정

    try:
        spare = "empty"
        # keyValue = cv2.waitKey(1) #키보드 입력대기
        ret, img = cap.read()
        h, w, _ = img.shape
        cx = h / 2
        img = img[:, 200:200 + img.shape[0]]
        img = cv2.flip(img, 1)

        img_input = cv2.resize(img, size)
        img_input = cv2.cvtColor(img_input, cv2.COLOR_BGR2RGB)
        img_input = (img_input.astype(np.float32) / 127.0) - 1
        img_input = np.expand_dims(img_input, axis=0)
        cv2.imshow('pre', img_input)  # 'pre' = 창제목 으로 창 띄워 보여주기
        prediction = model_spare.predict(img_input)
        idx = np.argmax(prediction)

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

    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    spare_capture()
    cv2.destroyAllWindows()
