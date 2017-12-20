import cv2
import csv
import sys
import numpy as np

def main(argv):
   faces = []
   labels = []
   face_recognizer = cv2.face.LBPHFaceRecognizer_create()
   #read csv file
   with open(argv[1], 'r') as csvfile:
      imageNames = csv.reader(csvfile, delimiter=';')
      for row in imageNames:
         faces.append(cv2.imread(row[0], 0))
         labels.append(int(row[1]))
   #train model
   face_recognizer.train(faces, np.array(labels))
   #save model in file
   face_recognizer.save("faceModels.yml")

if __name__ == "__main__":
   main(sys.argv)