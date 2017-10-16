import cv2
import picamera
import picamera.array

print("Initializing camera")
camera = picamera.PiCamera()
rawCapture = picamera.array.PiRGBArray(camera)

avg = None

for f in camera.capture_continuous(rawCapture, 'bgr', use_video_port=True):
   #grab frame
   frame = f.array

   # make frame smaller and create grayscale
   # frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
   gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
   gray = cv2.GaussianBlur(gray, (21, 21), 0)
   
   if avg is None:
      print("Starting background model")
      avg = gray.copy().astype("float")
      rawCapture.truncate(0)
      continue
      
   cv2.accumulateWeighted(gray, avg, 0.5)
   frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))
   
   thresh = cv2.threshold(frameDelta, 5, 255, cv2.THRESH_BINARY)[1]
   thresh = cv2.dilate(thresh, None, iterations=2)
   image, cnts, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
   
   for c in cnts:
      if cv2.contourArea(c) < 5000:
         continue
         
      (x, y, w, h) = cv2.boundingRect(c)
      cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
   
   cv2.imshow("Feed", frame)
   # cv2.imshow("Difference", frameDelta)
   if cv2.waitKey(1) & 0xFF == ord('q'):
      break
   rawCapture.seek(0)
   rawCapture.truncate()

cv2.destroyAllWindows()