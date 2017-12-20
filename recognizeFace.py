import sys
import cv2

def recognize(image):
   names = ["Hayden", "Lincoln"]
   face_recognizer = cv2.face.LBPHFaceRecognizer_create()
   face_recognizer.read("faceModels.yml")
   face_recognizer.setThreshold(29)

   result = face_recognizer.predict(image)
   if result[0] == -1:
      print("Not recognized")
   else:
      print(names[result[0]])

