import cv2
import sys

face_cascade = cv2.CascadeClassifier('/home/lincolntran/opencv/data/haarcascades/haarcascade_frontalface_default.xml')

def main(argv):
   #open original image
   img = cv2.imread(argv[1])
   gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

   #detect face in image (should be only one face)
   faces = face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(100, 100))

   #crop out face from image
   imgCrop(argv[1], img, faces)

def imgCrop(name, image, cropBox):
   i = 0
   for (x, y, w, h) in cropBox:
      cv2.imwrite(str(i) + name, image[y : y + h, x : x + w])
      i += 1

if __name__ == "__main__":
   main(sys.argv)