import sys
import cv2

def main(argv):
   names = ["Hayden", "Lincoln"]
   face_recognizer = cv2.face.LBPHFaceRecognizer_create()
   face_recognizer.read(argv[1])
   face_recognizer.setThreshold(27.2)

   image = cv2.imread(argv[2], 0)
   result = face_recognizer.predict(image)
   if result[0] == -1:
      print("Not recognized")
   else:
      print(names[result[0]])

if __name__ == "__main__":
   main(sys.argv)
