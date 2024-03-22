import easyocr
import cv2
import numpy as np
# from matplotlib import pyplot as plt

reader = easyocr.Reader(['en'])
 # ip = "https://192.168.43.252:8080/video"
# ip = "http://192.168.52.3:8080/video"
cap = cv2.VideoCapture(0)
# img = cv2.imread("ocr_test.jpeg")

while True:
    cur, img = cap.read()
    # img = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    out = reader.readtext(img)
    try:
        for i in out:
            top_left = tuple((int(val) for val in i[0][0]))
            bottom_right = tuple((int(val) for val in i[0][2]))
            text = i[1]
            img = cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 5)
            img = cv2.putText(img, text, top_left, cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 2)

        # print(out)
        # print(len(out))
        # for i in range(len(out)):
        #     text = out[i][-2]
        #     print(text)
    except:
        print("no data to display")

    cv2.imshow("cur",img)
    cv2.waitKey(1)
