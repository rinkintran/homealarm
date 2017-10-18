import cv2
import picamera
import picamera.array

face_cascade = cv2.CascadeClassifier('/home/pi/opencv/data/haarcascades/haarcascade_frontalface_default.xml')

print("Initializing camera")
camera = picamera.PiCamera()
rawCapture = picamera.array.PiRGBArray(camera)

for f in camera.capture_continuous(rawCapture, 'bgr', use_video_port=True):
   frame = f.array
   gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

   #find faces
   faces = face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(30, 30))

   for (x, y, w, h) in faces:
      cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

   cv2.imshow('Faces', frame)
   if cv2.waitKey(1) & 0xFF == ord('q'):
      break
   rawCapture.seek(0)
   rawCapture.truncate()

cv2.destroyAllWindows()