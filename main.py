import face_recognition
import numpy as np
import cv2
from datetime import datetime
import os


path = "images"
images = []
classmates = []
mylist = os.listdir(path)
# print(mylist)
for i in mylist:
    curimg = cv2.imread(f'{path}/{i}')
    images.append(curimg)
    classmates.append(os.path.splitext(i)[0])
# print(classmates)


def findencodings(images):
    encodinglist=[]
    for img in images:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodinglist.append(encode)
    return encodinglist

def markatten(name):
    with open('attendance.csv','r+') as f:
        mydata=f.readlines()
        namelist=[]
        for line in mydata:
            entry=line.split(',')
            namelist.append(entry[0])
        if name not in namelist:
            now=datetime.now()
            dtstring=now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtstring}')


encodelistknown=findencodings(images)

cap=cv2.VideoCapture(0,cv2.CAP_DSHOW)

while True:

    success,img=cap.read()
    small=cv2.resize(img,(0,0),None,0.25,0.25)
    small=cv2.cvtColor(small,cv2.COLOR_BGR2RGB)

    face_loactions = face_recognition.face_locations(small)
    face_ncodings = face_recognition.face_encodings(small, face_loactions)



    for enface,loface in zip(face_ncodings,face_loactions):
        match=face_recognition.compare_faces(encodelistknown,enface)
        dis=face_recognition.face_distance(encodelistknown,enface)
        index=np.argmin(dis)
        # print(index)

        if match[index]:
            name=classmates[index].upper()
            print(name)

            y1,x2,y2,x1=loface
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 255, 0),cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)



    cv2.imshow("web",img)
    cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()