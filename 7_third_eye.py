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
#: 

#----------------------------- :: Pins 
#::: Ultrasonic 
GPIO_TRIGGER = 18              # trigger
GPIO_ECHO = 24                 # Echo 

#::: Buzzer
BuzzerPin = 4

#----------------------------- :: Methods 
def weather():

  text = "for your weather update"
  speak(text)
  
  url = 'https://api.openweathermap.org/data/2.5/weather?lat=-25.7523712&lon=29.715950&appid=95b9aaca4c4d70262e60f63f8f3393ff'
  myobj = {'somekey': 'somevalue'}

  x = requests.post(url, data = myobj)
  txt = x.text
  print(txt)
  
  data = json.loads(txt)
  print(data)
  
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
  
  desc = data["weather"]["description"]  
  text = "thus you can expect "  + desc
  speak(text)
  
  cds = data["clouds"].all  
  text = "width "  + str(cds) + " percent cloud cover "
  speak(text)
  
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
