import datetime
import face_recognition
import numpy as np

print("Initializing camera")
camera = picamera.PiCamera()
camera.resolution = (320, 240)
rawCapture = np.empty((240, 320, 3), dtype=np.uint8)

def main(argv):
   #recognize faces
   lincoln_image = face_recognition.load_image_file("knownFaces/lincoln1.jpg")
   unknown_image = face_recognition.load_image_file(argv[0])

   lincoln_encoding = face_recognition.face_encodings(lincoln_image)[0]

if __name__ == "__main__":
    main()