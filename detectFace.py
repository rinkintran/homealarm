import cv2
import picamera
import picamera.array
import datetime
import time
from webhook import sendImage
import webhook
import _thread
import numpy as np
from recognizeFace import recognize

face_cascade = cv2.CascadeClassifier('/home/lincolntran/opencv/data/haarcascades/haarcascade_frontalface_default.xml')
eyes_cascade = cv2.CascadeClassifier('/home/lincolntran/opencv/data/haarcascades/haarcascade_eye.xml')

# Set up face recognizer object
names = ["Hayden", "Lincoln"]
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.read("faceModels.yml")
face_recognizer.setThreshold(29) #29 seems to work well

print("Initializing camera")
camera = picamera.PiCamera()
camera.exposure_mode = "sports"
camera.color_effects = (128,128)

log = open("log.txt", 'w')

def main():
   avg = None
   rawCapture = picamera.array.PiRGBArray(camera)
   # Continuous loop that constantly looks for changes in frames
   for f in camera.capture_continuous(rawCapture, 'bgr', use_video_port=True):
      frame = f.array

      # Convert to grayscale and blur a little bit
      gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      gray = cv2.GaussianBlur(gray, (21, 21), 0)
      
      # Keep track of rolling average to compare against
      if avg is None:
         print("Starting background model")
         avg = gray.copy().astype("float")
         rawCapture.truncate(0)
         continue

      # Find differences and create contour image
      cv2.accumulateWeighted(gray, avg, 0.5)
      frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))

      thresh = cv2.threshold(frameDelta, 5, 255, cv2.THRESH_BINARY)[1]
      thresh = cv2.dilate(thresh, None, iterations=2)

      image, cnts, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

      # If there are enough differences, process image
      if len(cnts) > 10:
         start = time.time()
         saveFace()
         end = time.time()
         print(end - start, "seconds")

      camera.resolution = (640, 480)
         
      rawCapture.seek(0)
      rawCapture.truncate()

   cv2.destroyAllWindows()

def saveFace():
   #set up camera specs
   camera.resolution = (1640, 1232)
   rawCapture = picamera.array.PiRGBArray(camera)

   camera.capture(rawCapture, 'bgr', use_video_port=True, splitter_port = 1)
   
   frame = rawCapture.array
   gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
   
   #find face in still
   faces = face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(100,100))
   
   #crop out face
   if len(faces) > 0:
      imgCrop(gray, faces)
   else:
      print("No face detected")
      log.write(datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S%p") + " Motion detected but no faces found, ignoring\n")

def imgCrop(image, cropBox):
   for (x, y, w, h) in cropBox:
      croppedFace = image[y : y + h, x : x + w]
      eyes = eyes_cascade.detectMultiScale(croppedFace)
      if len(eyes) > 0:
         print("Found good face with eyes")
         _thread.start_new_thread(recognize, (croppedFace, names, face_recognizer, log))
      else:
         print("Couldn't find eyes on the face")
         imgName = datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S%p")
         log.write(imgName + " Low quality face captured, alerting owner anyways\n")
         cv2.imwrite(imgName + ".jpg", croppedFace)
         _thread.start_new_thread(sendImage, ("Detected movement but couldn't identify a face", imgName, croppedFace))


if __name__ == "__main__":
    main()