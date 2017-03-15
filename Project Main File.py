import numpy as np
import smtplib, os
import datetime
import time
import numpy
import cv2
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.utils import COMMASPACE, formatdate
from email import encoders
#Where the specific files of facial and eye cascades are located in.
detectFace = cv2.CascadeClassifier('C:\\opencv\\build\\etc\\haarcascades\\haarcascade_frontalface_default.xml')
detectEyes = cv2.CascadeClassifier('C:\\opencv\\build\\etc\\haarcascades\\haarcascade_eye.xml')
#Starting to form the file in which the security footage is taken.
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('Security Footage.avi', fourcc, 5.0, (640,480))
start_time = 0
end_time = 0
firstFrame = None
#Locates the camera.
capture = cv2.VideoCapture(0)
isRecording = False

while(True):
    # Capture frame-by-frame
    (grabbed, frame) = capture.read()
    (grabbed2, frame2) = capture.read()
    ret, frame1 = capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  #Converting to Greyscale.
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    frameDelta = cv2.absdiff(gray, gray2)
    ret, frameDelta = cv2.threshold(frameDelta, 5, 1, cv2.THRESH_BINARY)
    #Taking the average of the 3 RGB values and taking them to form one Integer.
    #Which is the percentage of pixel change.
    finalPixel = ((np.sum(frameDelta) / np.size(frameDelta)) * 100) 

    #If the pixels start to change then start recrding the frames to a file for 10 seconds.
    if (finalPixel > 30 and not isRecording):
            start_time = time.time()
            isRecording = True
    if (isRecording):
        out.write(frame)

    end_time = time.time()
    elapsed_time = end_time - start_time
    if(isRecording and elapsed_time >= 10):
        out.release()
        isRecording = False
        
    #Face Detection starts here
    faces = detectFace.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0),2)
        g = gray[y: y+h, x: x+w]
        color = frame[y: y+h, x: x+w]
        eyes = detectEyes.detectMultiScale(g)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(color,(ex,ey),(ex+ew, ey+eh),(0,255,0),2)
    #Converting the finalPixel value into a float and taking it as a text.
    text = ((np.sum(frameDelta) / np.size(frameDelta)) * 100)
    text = float("{0:.2f}".format(text))
    #Where and what kind of font to display the Pixel Change in the frame.    
    cv2.putText(frame, "Pixels Changed: {}".format(text), (10,20),
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0),2)
    cv2.putText(frame2, "Pixels Changed: {}".format(text), (10,20),
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0),2)
    #Displays time and date.
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
               (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75,
               (0,255,0),1)
    cv2.putText(frame2, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
               (10, frame2.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75,
               (0,255,0),1)
    #Show the feed of the actual camera.
    cv2.imshow("Security Camera", frame)
    #Stops the program if 'q' is pressed.       
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
#When the video is saved to the file and the video feed is over send it to an email.
#From where and to who you are sending it to.
from_address = "cst205team33@gmail.com"
to_address = "oscarsramirez@student.hartnell.edu"

#Part where the email is structured.
msg = MIMEMultipart()
msg['From'] = from_address
msg['To'] = COMMASPACE.join(to_address)
msg['Date'] = formatdate(localtime = True)
msg['Subject'] = "Security Footage"

body = "Here is the file of the footage"

msg.attach(MIMEText(body))
#Getting the file of the video taken previously.
part = MIMEBase('application', 'octet-stream')
part.set_payload(open("Security Footage.avi", "rb").read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', 'attachment; filename= "Security Footage.avi"')
msg.attach(part)
#Setting up the port and server and where to send the video file. 
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(from_address, "SecurityCam")
text = msg.as_string()
server.sendmail(from_address, to_address, text)
server.quit()

# When everything done, release the capture
capture.release()
cv2.destroyAllWindows()