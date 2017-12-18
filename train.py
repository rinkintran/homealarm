import cv2
import csv
import sys
import numpy as np

def main(argv):
   face_recognizer = cv2.face.LBPHFaceRecognizer_create()
   #read csv file
   with open(argv[1], 'r') as csvfile:
      imageNames = csv.reader(csvfile, delimiter=':')
      for row in imageNames:
         print(row)
   #train model
   # face_recognizer.train(faces, np.array(labels))
   #save model in file

   return

def readMap():
   return

if __name__ == "__main__":
   main(sys.argv)