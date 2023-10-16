# Author : Thubakgale Mabalane 
# Date : 16/10/2023
#::: OpenCV Facial Recognition Example 
#----------------------------- :: Modules
#:: op
import cv2 #For Image processing 
import numpy as np #For converting Images to Numerical array 
import os #To handle directories 
from PIL import Image #Pillow lib for handling images
#:: Camera
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
# 

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
# allow the camera to warmup
time.sleep(0.1)

# https://www.geeksforgeeks.org/face-detection-using-cascade-classifier-using-opencv-python/
#----------------------------- :: Methods 
def face_train():
  
  face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
  recognizer = cv2.face.LBPHFaceRecognizer_create()

  Face_ID = -1 
  pev_person_name = ""
  y_ID = []
  x_train = []

  Face_Images = os.path.join(os.getcwd(), "dataset") #Tell the program where we have saved the face images 
  print (Face_Images)

  for root, dirs, files in os.walk(Face_Images): #go to the face image directory 
    for file in files: #check every directory in it 
      if file.endswith("jpeg") or file.endswith("jpg") or file.endswith("png"): #for image files ending with jpeg,jpg or png 
        path = os.path.join(root, file)
        person_name = os.path.basename(root)
        print(path, person_name)

      if pev_person_name!=person_name: #Check if the name of person has changed 
        Face_ID=Face_ID+1 #If yes increment the ID count 
        pev_person_name = person_name

      Gery_Image = Image.open(path).convert("L") # convert the image to greysclae using Pillow
      Crop_Image = Gery_Image.resize( (800,800) , Image.ANTIALIAS) #Crop the Grey Image to 550*550 (Make sure your face is in the center in all image)
      Final_Image = np.array(Crop_Image, "uint8")
      #print(Numpy_Image)
      faces = face_cascade.detectMultiScale(Final_Image, scaleFactor=1.5, minNeighbors=5) #Detect The face in all sample image 
      print (Face_ID,faces)

      for (x,y,w,h) in faces:
        roi = Final_Image[y:y+h, x:x+w] #crop the Region of Interest (ROI)
        x_train.append(roi)
        y_ID.append(Face_ID)

  recognizer.train(x_train, np.array(y_ID)) #Create a Matrix of Training data 
  recognizer.save("face-trainner.yml") #Save the matrix as YML file 

  pass

def face_recognize():
  labels = ["Limpho Letsoisa"] 

  face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
  recognizer = cv2.face.LBPHFaceRecognizer_create()
  recognizer.read("face-trainner.yml")

  # capture frames from the camera
  for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array

    # show the frame
    img = image 
    
    gray  = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #convert Video frame to Greyscale
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5) #Recog. faces
    
    for (x, y, w, h) in faces:
    
      roi_gray = gray[y:y+h, x:x+w] #Convert Face to greyscale 
      id_, conf = recognizer.predict(roi_gray) #recognize the Face

      if conf>=80:
        font = cv2.FONT_HERSHEY_SIMPLEX #Font style for the name 
        name = labels[id_] #Get the name from the List using ID number
        cv2.putText(img, name, (x,y), font, 1, (0,0,255), 2)
        
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

    cv2.imshow("Preview", img)
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break 

  # When everything done, release the capture
  cap.release()
  cv2.destroyAllWindows()
  pass
  
def face_interpret():
  pass
# ---------------------------- :: Setup
def my_setup():

  print("Training Model")
  face_train()
  print("Set Up")
  pass
#------------------------------:: Loop
def my_loop():
  print("Recognize")
  face_recognize()
  print("Loop after 10 second")
  time.sleep(10)
  
  pass 
#------------------------------:: Main 
# Main function
def main () :
# Setup 
 my_setup()
# Infinite loop
 while 1 : 
  my_loop()
  pass
# Command line execution
if __name__ == '__main__' :
   main()
