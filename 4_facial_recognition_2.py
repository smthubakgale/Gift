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

#----------------------------- :: PINS
#:": Ultrasonic 
GPIO_TRIGGER = 18              # trigger
GPIO_ECHO = 24                 # Echo 

#::: Buzzer
BuzzerPin = 4

#----------------------------- :: Variables
#::: Text-To-Speech
cmd_beg= 'espeak '
cmd_end= ' | aplay Text.wav  2>/dev/null' 
cmd_out= '--stdout > Text.wav ' 

#::: Camera 
camera = PiCamera()

#----------------------------- :: Methods 
def face_recognize():
  #-------------::: 1. cascade for face detection
  encoding = "encodings.pickle"
  cascade = "haarcascade_frontalface_default.xml"
  
  print("[INFO] loading encodings + face detector...")
  data = pickle.loads(open(encoding, "rb").read())
  detector = cv2.CascadeClassifier(cascade)

  #-------------::: 2. initialize the video stream  
  print("[INFO] starting video stream...")
  #vs = VideoStream(src=0).start()                # webcam
  vs = VideoStream(usePiCamera=True).start()      # picamera 
  time.sleep(2.0)
  
  # start the FPS counter
  fps = FPS().start()

  #-------------::: 3. loop over video stream file frames 
  while True:
  	# grab the frame from the threaded video stream and resize it
  	# to 500px (to speedup processing)
  	frame = vs.read()
  	frame = imutils.resize(frame, width=500)
  	
  	# convert the input frame from (1) BGR to grayscale (for face
  	# detection) and (2) from BGR to RGB (for face recognition)
  	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  	rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
  
  	# detect faces in the grayscale frame
  	rects = detector.detectMultiScale(gray, scaleFactor=1.1, 
  		minNeighbors=5, minSize=(30, 30))
  
  	# OpenCV returns bounding box coordinates in (x, y, w, h) order
  	# but we need them in (top, right, bottom, left) order, so we
  	# need to do a bit of reordering
  	boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]
  
  	# compute the facial embeddings for each face bounding box
  	encodings = face_recognition.face_encodings(rgb, boxes)
  	names = []
    
    # loop over the facial embeddings
  	for encoding in encodings:
  		# attempt to match each face in the input image to our known
  		# encodings
  		matches = face_recognition.compare_faces(data["encodings"],
  			encoding)
  		name = "Unknown"
  
  		# check to see if we have found a match
  		if True in matches:
  			# find the indexes of all matched faces then initialize a
  			# dictionary to count the total number of times each face
  			# was matched
  			matchedIdxs = [i for (i, b) in enumerate(matches) if b]
  			counts = {}
  
  			# loop over the matched indexes and maintain a count for
  			# each recognized face face
  			for i in matchedIdxs:
  				name = data["names"][i]
  				counts[name] = counts.get(name, 0) + 1
  
  			# determine the recognized face with the largest number
  			# of votes (note: in the event of an unlikely tie Python
  			# will select first entry in the dictionary)
  			name = max(counts, key=counts.get)
  		
  		# update the list of names
  		names.append(name)

  pass
def face_embeddings(): 
  #-------------::: 1. Get the paths to the images files
  # dataset paths
  dataset = "dataset"
  imagePaths = list(paths.list_images(dataset))

  # initialize the list of known encodings and known names
  knownEncodings = []
  knownNames = []
  
  #-------------::: 2. Extract facial Encodings and Names from paths
  # loop over the image paths
  for (i, imagePath) in enumerate(imagePaths):
  	# extract the person name from the image path
  	print("[INFO] processing image {}/{}".format(i + 1,
  		len(imagePaths)))
    
  	name = imagePath[:-4] 
  
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
    
  #-------------::: 3. Export facial encodings and names to disk  
  encoding = "encodings.pickle"
  print("[INFO] serializing encodings...")
  data = {"encodings": knownEncodings, "names": knownNames}
  f = open(encoding, "wb")
  f.write(pickle.dumps(data))
  f.close()
  #-------------::: 
  
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

  # Facial Recognition
  face_embeddings()
  face_recognize()
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
