import numpy as np
import datetime
import numpy
import cv2

capture = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640,480))
count = 0
firstFrame = None

while(True):
    # Capture frame-by-frame
    (grabbed, frame) = capture.read()
    (grabbed2, frame2) = capture.read()
    ret, frame1 = capture.read()
    diff = frame - frame2
    avg_color_row = numpy.average(diff, axis = 0)
    avg_color = numpy.average(avg_color_row, axis = 0)
    #count +=1
    #diff = (diff)/(count * 100)
            
    if not grabbed:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21,21),0)
    if not grabbed2:
        break
    gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21,21),0)

    if firstFrame is None:
        firstFrame = gray
        continue
    frameDelta = cv2.absdiff(firstFrame, gray)
    threshold = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
    threshold = cv2.dilate(threshold, None, iterations = 2)
    (cnts, _, _) = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)
    for a in cnts:
        (x,y,w,h) = cv2.boundingRect(a)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
        cv2.rectangle(frame2, (x,y), (x+w, y+h), (0,255,0), 2)
        text = avg_color
        
    cv2.putText(frame, "Room Status: {}".format(text), (10,20),
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0),2)
    cv2.putText(frame2, "Room Status: {}".format(text), (10,20),
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0),2)
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
               (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75,
               (0,255,0),1)
    cv2.putText(frame2, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
               (10, frame2.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75,
               (0,255,0),1)
        
    cv2.imshow("Security Camera", frame)
    cv2.imshow("Threshold", threshold)
    cv2.imshow("Delta Frame", frameDelta)
    while(capture.isOpened()):
        if ret == True:
            out.write(frame1)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            else:
                break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
capture.release()
out.release()
cv2.destroyAllWindows()
