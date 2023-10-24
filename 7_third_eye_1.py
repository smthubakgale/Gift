# Author : Thubakgale Mabalane 
# Date : 17/10/2023
#::: Third Eeye Project  
#----------------------------- :: Modules
#: basics 
import RPi .GPIO as GPIO 
import time 
#: text to speech 
from num2words import num2words
#: command line 
from subprocess import call
#: get request
import requests
#: json
import json
#:: facial recognition 
import cv2 #For Image processing 
import numpy as np #For converting Images to Numerical array 
import os #To handle directories 
from PIL import Image #Pillow lib for handling images
#:: Camera
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
#:: Multithreading
import threading
#: 
 
#----------------------------- :: Pins 
#::: Ultrasonic 
GPIO_TRIGGER = 18              # trigger
GPIO_ECHO = 24                 # Echo 

#::: Buzzer
BuzzerPin = 4 

#----------------------------- :: Methods 
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

  # initialize the camera and grab a reference to the raw camera capture
  camera = PiCamera()
  camera.resolution = (640, 480)
  camera.framerate = 32
  rawCapture = PiRGBArray(camera, size=(640, 480))
  # allow the camera to warmup
  time.sleep(0.1)

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
 
      print(conf)
      if conf>=80:
        print(id_)
        font = cv2.FONT_HERSHEY_SIMPLEX #Font style for the name 
        name = labels[id_] #Get the name from the List using ID number
        cv2.putText(img, name, (x,y), font, 1, (0,0,255), 2)
        print(name)
        text = name + " is infront of you"
        speak(text)
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
      else :
        text = "unknown person infront of you"
        speak(text)
    #cv2.imshow("Preview", img)
    key = cv2.waitKey(1) & 0xFF
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break 

  # When everything done, release the capture
  cap.release()
  cv2.destroyAllWindows()
  pass
  
def weather():

  text = "for your weather update"
  speak(text)
  
  url = 'https://api.openweathermap.org/data/2.5/weather?lat=-25.7523712&lon=29.715950&appid=95b9aaca4c4d70262e60f63f8f3393ff'
  myobj = {'somekey': 'somevalue'}

  x = requests.post(url, data = myobj)
  txt = x.text 
  
  data = json.loads(txt)  
  main = data["main"]  
  
  temp = round(main["temp"] - 273.15 , 2)  
  text = "the temperature is " + str(temp) + " degree celcius"
  speak(text)
  
  temp = round(main["temp_min"] - 273.15 , 2)  
  text = "with a minimum of "  + str(temp) + " degree celcius"
  speak(text)
  
  temp = round(main["temp_max"] - 273.15 , 2)   
  text = "and a maximum of "  + str(temp) + " degree celcius"
  speak(text)
    
  wind_speed = data["wind"]["speed"]  
  text = "the wind speed is "  + str(wind_speed) + " metres per second "
  speak(text)
  
  cds = data["clouds"]["all"]  
  text = "with "  + str(cds) + " percent cloud cover "
  speak(text)
  
  text = "thus you can expect "  
  speak(text)
  
  for wd in data["weather"] :
 
    desc = wd["description"]   
    speak(desc)
  
  pass
  
def buzz_sound(song , beat):
  
  Buzz = GPIO.PWM(BuzzerPin, 440)
  Buzz.start(60) 
   
  for i in range(1, len(song)):
    if song[i] != 0 : 
      Buzz.ChangeFrequency(song[i])
    else: 
      time.sleep(beat[i]*0.13) 

  Buzz.stop()
  pass
  
def speak(txt):

  cmd_beg= 'espeak '
  cmd_end= ' | aplay Text.wav  2>/dev/null' 
  cmd_out= '--stdout > Text.wav ' 

  arr = txt.split()
  
  for text in arr: 
    call([cmd_beg+cmd_out+text+cmd_end], shell=True)
    
  pass
  
def obst():
  
  d = distance()
  
  if d < 50 :
    b1 = [ 5 , 5 , 5 , 5 , 5 , 5  ] # time
    f1 = [ 0 , 1 , 0 , 1 , 0 , 1  ] # frequency 
  
    buzz_sound(f1 , b1);
    text = "collision emminent"
    speak(text)
  elif d < 150 :
    dist = round(d) 
    text = "object detected " + str(dist) + " centimetres away"
    speak(text)
   
  pass
  
def distance():
  
  #--- send trigger for 0.01 ms
  GPIO.output(GPIO_TRIGGER, True) 
  time.sleep(0.00001)
  GPIO.output(GPIO_TRIGGER, False)

  #--- measure echo duration 
  StartTime = time.time()
  StopTime = time.time()
 
  #:: save StartTime
  while GPIO.input(GPIO_ECHO) == 0:
     StartTime = time.time()
 
  #:: save time of arrival
  while GPIO.input(GPIO_ECHO) == 1:
     StopTime = time.time()
 
  #:: time difference between start and arrival : divide by 2 
  TimeElapsed = (StopTime - StartTime)/2
  
  # total distance = total time * sonic speed (34300 cm/s))
  distance = (TimeElapsed * 34300) 
  #---
  
  return distance 
  pass
# ---------------------------- :: Setup
def my_setup():

  #: basics
  GPIO.setmode(GPIO.BCM)
  GPIO.setwarnings(False)
  #: ultrasonic 
  GPIO.setup(18, GPIO.OUT)           # Ultrasound trigger
  GPIO.setup(24, GPIO.IN)            # Ultrasound Echo 
  #: Buzzer
  GPIO.setup(BuzzerPin, GPIO.OUT) 
  #:..
  print("Weather")
  weather()
  
  print("Training Model")
  face_train()

  print("Recognise")
  t1 = threading.Thread(target=face_recognize, args=())
  t1.start()
  
  print("Set Up")
  
  pass
#------------------------------:: Loop
def my_loop():

  print("Loop Start")
  obst()
  
  print("Loop after 10 second")
  time.sleep(3)
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
