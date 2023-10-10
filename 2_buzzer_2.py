# Author : Thubakgale Mabalane 
# Date : 10/10/2023
#::: Ultrasonic + Buzzer Example 
#----------------------------- :: Modules
import RPi .GPIO as GPIO 
import time 

#----------------------------- :: PINS
#:": Ultrasonic 
GPIO_TRIGGER = 18              # trigger
GPIO_ECHO = 24                 # Echo 

#::: Buzzer
global Buzz 
BuzzerPin = 4

#----------------------------- :: Variables


#----------------------------- :: Methods 
def buzz_sound(song , beat):
   
  Buzz = GPIO.PWM(BuzzerPin, 440) 
  Buzz.start(50) 
   
  for i in range(1, len(song)):
     Buzz.ChangeFrequency(song[i])
     time.sleep(beat[i]*0.13) 
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

  b1 = [8,8,8,8,]
  f1 = [2600 , 600 , 2600 , 600]
  
  buzz_sound(f1 , b1);
  
  dist = distance()

  print(str(dist))
  
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
