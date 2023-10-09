# Author : Thubakgale Mabalane 
# Date : 09/10/2023
#::: Ultrasonic Example 
#----------------------------- :: Modules
import RPi .GPIO as GPIO 
import time 

#----------------------------- :: Methods 
def distance():
  return 5
  pass
# ---------------------------- :: Setup
def my_setup():

  GPIO.setmode(GPIO.BCM)
  GPIO.setwarnings(False)
  
  GPIO.setup(18, GPIO.OUT)    # Ultrasound trigger
  GPIO.setup(24, GPIO.IN)     # Ultrasound Echo 

  print("Set Up")
  pass
#------------------------------:: Loop
def my_loop():

  dist = distance()

  println("distance : " % dist)
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
