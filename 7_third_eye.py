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

#----------------------------- :: Pins 
#:": Ultrasonic 
GPIO_TRIGGER = 18              # trigger
GPIO_ECHO = 24                 # Echo 

#----------------------------- :: Variables
#::: Text-To-Speech
cmd_beg= 'espeak '
cmd_end= ' | aplay Text.wav  2>/dev/null' 
cmd_out= '--stdout > Text.wav ' 

#----------------------------- :: Methods 
def speak(txt):
  
  arr = txt.split()
  
  for text in arr: 
    call([cmd_beg+cmd_out+text+cmd_end], shell=True)
    
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
  GPIO.setup(18, GPIO.OUT)    # Ultrasound trigger
  GPIO.setup(24, GPIO.IN)     # Ultrasound Echo 
  #:..
  print("Set Up")
  pass
#------------------------------:: Loop
def my_loop():

  dist = distance()
  text = "object detected " + str(dist) + " centimetres away "

  print(str(dist))
  
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
