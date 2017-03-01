#this is the face detect

import cv2
import numpy as np

faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cam = cv2.VideoCapture(0)

id = raw_input("Enter user ID\n")
num = 0
while(True):
    ret,img = cam.read();
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces=faceDetect.detectMultiScale(gray,1.3,5)
    for (x,y,w,h) in faces:
        num+=1
        cv2.imwrite("dataSet/User."+str(id)+ "."+str(num)+".jpg", gray[y:y+h,x:x+w])
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        cv2.waitKey(100)
    cv2.imshow("Face",img)
    cv2.waitKey(1)
    if (num > 20):
        break;
        
cam.release()
cv2.destroyAllWindows()


#this is the facial recognition

import os
import cv2
import numpy as np
from PIL import Image

recognizer = cv2.createLBPHFaceRecognizer();
path = "dataset"

def getImageWithID(path):
    imagePath = [os.path.join(path,f) for f in os.listdir(path)]
    faces = []
    IDs = []
    for imagePath in imagePaths:
        faceImg = Image.open(imagePath).conver("L")
        faceNp = np.array(faceImg,"unit8")
        ID = int(os.path.split(ImagePath)[-1].split(".")[1])
        faces.append(faceNp)
        IDs.append(ID)
        cv2.imshow("trans", faceNP)
        cv2.waitKey(10)
    return np.array(IDs), faces

faces,Ids=getImagesWithID(path)
recognition.train(faces,Ids)
recognition.save("FaceRe/transData.yml")
cv2.destroyAllWindows()