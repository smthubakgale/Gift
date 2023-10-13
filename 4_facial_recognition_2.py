# Author : Thubakgale Mabalane 
# Date : 13/10/2023
#::: Ultrasonic + Buzzer + Text-To-Speech + Facial Recognition Example 
#----------------------------- :: Modules
#:: Ultrasonic + Buzzer
import RPi .GPIO as GPIO 
import time 
#:: Text-to-Speech
from num2words import num2words
from subprocess import call
#:: Camera 
from picamera import PiCamera
#::  Facial Recognition
from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os

#----------------------------- :: PINS
#:": Ultrasonic 
GPIO_TRIGGER = 18              # trigger
GPIO_ECHO = 24                 # Echo 

#::: Buzzer
BuzzerPin = 4

#----------------------------- :: Variables
#::: Text-To-Speech
cmd_beg= 'espeak '
cmd_end= ' | aplay /home/pi/Documents/Text.wav  2>/dev/null' 
cmd_out= '--stdout > /home/pi/Documents/Text.wav ' 

#::: Camera 
camera = PiCamera()

#----------------------------- :: Methods 
def face_recog(): 
  #------------- 1. 
  # dataset paths
  dataset = "/home/pi/Documents/dataset"
  imagePaths = list(paths.list_images(dataset))

  # initialize the list of known encodings and known names
  knownEncodings = []
  knownNames = []

  #------------- 2. 
  # loop over the image paths
  for (i, imagePath) in enumerate(imagePaths):
  	# extract the person name from the image path
  	print("[INFO] processing image {}/{}".format(i + 1,
  		len(imagePaths)))
  	name = imagePath.split(os.path.sep)[-2]
  
  	# load the input image and convert it from BGR (OpenCV ordering)
  	# to dlib ordering (RGB)
  	image = cv2.imread(imagePath)
  	rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
  
  	# detect the (x, y)-coordinates of the bounding boxes
  	# corresponding to each face in the input image
  	boxes = face_recognition.face_locations(rgb,
  		model=args["detection_method"])
  
  	# compute the facial embedding for the face
  	encodings = face_recognition.face_encodings(rgb, boxes)
  
  	# loop over the encodings
  	for encoding in encodings:
  		# add each encoding + name to our set of known names and
  		# encodings
  		knownEncodings.append(encoding)
  		knownNames.append(name)
      
  pass
def buzz_sound(song , beat):
  
  Buzz = GPIO.PWM(BuzzerPin, 440)
  Buzz.start(60) 
   
  for i in range(1, len(song)):
     if song[i] != 0 :
        Buzz.start(60) 
        Buzz.ChangeFrequency(song[i])
     else:
          Buzz.stop()
     time.sleep(beat[i]*0.13) 

  Buzz.stop()
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

  GPIO.setmode(GPIO.BCM)
  GPIO.setwarnings(False)
  
  GPIO.setup(GPIO_TRIGGER, GPIO.OUT)   
  GPIO.setup(GPIO_ECHO , GPIO.IN)   
  
  GPIO.setup(BuzzerPin, GPIO.OUT) 
   
  print("Set Up")
  pass
#------------------------------:: Loop
def my_loop():
  
  # Buzzer
  b1 = [ 5 , 5 , 5 , 5 , 5 , 5  ] # time
  f1 = [ 0 , 1 , 0 , 1 , 0 , 1  ] # frequency 
  
  buzz_sound(f1 , b1);
  # Ultrasonic
  dist = distance()

  print(str(dist))
  # Text to Speech
  text = "Hello World";
  call([cmd_beg+cmd_out+text+cmd_end], shell=True)

  # Camera 
  camera.start_preview()
  time.sleep(1)
  camera.capture('/home/pi/Documents/capture/capture.jpg')
  camera.stop_preview()

  #
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