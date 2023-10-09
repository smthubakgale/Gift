# Author : Thubakgale Mabalane 
# Date : 09/10/2023
#::: Ultrasonic Example 
#----------------------------- :: Modules
import RPi .GPIO as GPIO 
import time 

#----------------------------- :: PINS
#:": Ultrasonic 
GPIO_TRIGGER = 18              # trigger
GPIO_ECHO = 24                 # Echo 

#----------------------------- :: Methods 
def distance():
  
  #--- send trigger for 0.01 ms
  GPIO.output(GPIO_TRIGGER, True) 
  time.sleep(0.00001)
  GPIO.output(GPIO_TRIGGER, False)
 
  StartTime = time.time()
  StopTime = time.time()
 
  # save StartTime
    while GPIO.input(24) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
  return 5
  pass
# ---------------------------- :: Setup
def my_setup():

  GPIO.setmode(GPIO.BCM)
  GPIO.setwarnings(False)
  
  GPIO.setup(GPIO_TRIGGER, GPIO.OUT)   
  GPIO.setup(GPIO_ECHO , GPIO.IN)     

  print("Set Up")
  pass
#------------------------------:: Loop
def my_loop():

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
