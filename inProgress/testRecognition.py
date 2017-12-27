import sys
import cv2
from webhook import sendImage
import webhook
import _thread
import datetime


def main(argv):
   names = ["Hayden", "Lincoln"]
   face_recognizer = cv2.face.LBPHFaceRecognizer_create()
   face_recognizer.read("../faceModels.yml")
   face_recognizer.setThreshold(27.2)

   image = cv2.imread(argv[1], 0)
   result = face_recognizer.predict(image)
   if result[0] == -1:
      print("Not recognized")
   else:
      print(names[result[0]])
      sendImage("test", argv[1], image)


if __name__ == "__main__":
   main(sys.argv)
