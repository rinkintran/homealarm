import sys
import cv2
import datetime
from webhook import sendImage
import webhook
import _thread

def recognize(image, names, face_recognizer, log):
   # names = ["Hayden", "Lincoln"]
   # face_recognizer = cv2.face.LBPHFaceRecognizer_create()
   # face_recognizer.read("faceModels.yml")
   # face_recognizer.setThreshold(29)

   result = face_recognizer.predict(image)
   if result[0] == -1:
      print("Not recognized")
      imgName = datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S%p")
      log.write(imgName + " Face not recognized, alerting owner\n")
      cv2.imwrite(imgName + ".jpg", image)
      _thread.start_new_thread(sendImage, ("Couldn't identify person!", imgName, image))
   else:
      print(names[result[0]])
      log.write(datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S%p") + " Detected " + names[result[0]] + "\n")


