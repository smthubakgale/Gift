# Author : Thubakgale Mabalane 
# Date : 09/10/2023
#::: Ultrasonic Example 
#----------------------------- :: Modules
import RPi .GPIO as GPIO 
import time 

# ---------------------------- :: Setup
def my_setup():

  GPIO.setmode(GPIO.BCM)
  GPIO.setwarnings(False)

  print("Welcome to set up")
  pass
#------------------------------:: Loop
def my_loop():
  print("Loop after 1 second")
  time.sleep(1)
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
