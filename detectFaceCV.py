import cv2
import picamera
import picamera.array
import datetime
import io
import numpy as np

face_cascade = cv2.CascadeClassifier('/home/lincolntran/opencv/data/haarcascades/haarcascade_frontalface_default.xml')
eyes_cascade = cv2.CascadeClassifier('/home/lincolntran/opencv/data/haarcascades/haarcascade_eye.xml')

print("Initializing camera")
camera = picamera.PiCamera()

def main():
   rawCapture = picamera.array.PiRGBArray(camera)
   for f in camera.capture_continuous(rawCapture, 'bgr', use_video_port=True):
      frame = f.array
      gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

      #find faces
      faces = face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(30, 30))

      if len(faces) > 0:
         print(faces)
         saveFace()
         
      # for (x, y, w, h) in faces:
      #    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

      # cv2.imshow('Faces', frame)
      # if cv2.waitKey(1) & 0xFF == ord('q'):
      #    break
      rawCapture.seek(0)
      rawCapture.truncate()

   cv2.destroyAllWindows()

def imgCrop(image, cropBox):
   for (x, y, w, h) in cropBox:
      return image[y : y + h, x : x + w]

def saveFace():
   #capture high quality still
   camera.resolution = (2592, 1944)
   camera.iso = 800
   camera.shutter_speed = 16666
   with picamera.array.PiRGBArray(camera) as stream:
      camera.capture(stream, 'bgr', use_video_port=False, splitter_port = 2)
      frame = stream.array
      gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
   #find face in still
   faces = face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(60,60))
   #crop out face
   if len(faces) > 0:
      croppedFace = imgCrop(frame, faces)
      eyes = eyes_cascade.detectMultiScale(croppedFace)
      if len(eyes) > 0:
         cv2.imwrite(datetime.datetime.now().strftime("%I:%M:%S%p") + ".jpg", croppedFace)
      else:
         print("No eyes recognized on the face, bad picture")
   else:
      print("No faces recognized in still!")

   camera.resolution = (640,480)
   return

if __name__ == "__main__":
    main()