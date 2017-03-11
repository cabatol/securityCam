import numpy as np
import datetime
import time
import numpy
import cv2

detectFace = cv2.CascadeClassifier('C:\\opencv\\build\\etc\\haarcascades\\haarcascade_frontalface_default.xml')
detectEyes = cv2.CascadeClassifier('C:\\opencv\\build\\etc\\haarcascades\\haarcascade_eye.xml')
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('Security Footage.avi', fourcc, 5.0, (640,480))
t0 = time.time()
x = 0
y = 0
z = 0
firstFrame = None
capture = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    (grabbed, frame) = capture.read()
    (grabbed2, frame2) = capture.read()
    ret, frame1 = capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    frameDelta = cv2.absdiff(gray, gray2)
    ret, frameDelta = cv2.threshold(frameDelta, 5, 1, cv2.THRESH_BINARY)
    finalPixel = ((np.sum(frameDelta) / np.size(frameDelta)) * 100)

    if(finalPixel > 25):
        temp = t0 + 15
        while(t0 != temp):
            out.write(frame)
    
    if not grabbed:
        break
    
    gray = cv2.GaussianBlur(gray, (21,21),0)
    if not grabbed2:
        break
   
    gray2 = cv2.GaussianBlur(gray2, (21,21),0)
    
    if firstFrame is None:
        firstFrame = gray
        continue
    #Face Detection starts here
    faces = detectFace.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0),2)
        g = gray[y: y+h, x: x+w]
        color = frame[y: y+h, x: x+w]
        eyes = detectEyes.detectMultiScale(g)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(color,(ex,ey),(ex+ew, ey+eh),(0,255,0),2)
       
    text = ((np.sum(frameDelta) / np.size(frameDelta)) * 100)
    text = float("{0:.2f}".format(text))
        
    cv2.putText(frame, "Pixels Changed: {}".format(text), (10,20),
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (124,255,0),2)
    cv2.putText(frame2, "Pixels Changed: {}".format(text), (10,20),
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0),2)
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
               (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 0.75,
               (0,255,0),1)
    cv2.putText(frame2, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
               (10, frame2.shape[0] - 10), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 0.75,
               (0,255,0),1)
        
    cv2.imshow("Security Camera", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# When everything done, release the capture
capture.release()
out.release()
cv2.destroyAllWindows()

