# (C) Ihsan Topcu - Ihsansoft - 2021
# This code is free to use.
# Pull requests are appreciated.

from json.decoder import JSONDecodeError
from requests import api
from requests.models import Response
import RPi.GPIO as GPIO
import time
import requests
import os
import threading
from threading import Thread
import json

class CheckAPI(Thread):
  def run(self):
    try:
      global state
      while True:
        response = requests.get("http://" + Server + "/api/plugin/psucontrol", headers={'X-Api-Key':str(API_KEY)})
        JSONData = response.json()
        state = JSONData['isPSUOn']
        event.wait(3)
    except ConnectionRefusedError:
      print("Connection refused")
    except ConnectionError:
      print("Connection error")
    finally:
      exit
  
class CheckButton(Thread):
  def run(self):
    global state
    global buttonPin
    global GPIO
    global os
    while True:
      pinstate = GPIO.input(buttonPin)
      print(pinstate)
        if pinstate == 0:
          print("Button pressed")
          if (state == True):
            os.system("curl -s -H \"Content-Type: application/json\" -H \"X-Api-Key:"+ API_KEY +"\" -X POST -d '{ \"command\":\"turnPSUOff\" }\' -u username:password http://" + Server + "/api/plugin/psucontrol")
          else:
            os.system("curl -s -H \"Content-Type: application/json\" -H \"X-Api-Key:"+ API_KEY +"\" -X POST -d '{ \"command\":\"turnPSUOn\" }\' -u username:password http://" + Server + "/api/plugin/psucontrol")
      

try:
  API_KEY = "___API_KEY___"
  Server = "localhost"
  state = False
  event = threading.Event()

  buttonPin = 37
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(buttonPin,GPIO.IN,pull_up_down=GPIO.PUD_UP)
  Button = CheckButton()
  Api = CheckAPI()
  print("Activating threads")
  Button.start()
  Api.start()
  print(GPIO.input(buttonPin))

except KeyboardInterrupt:
  print("\nEXIT")
finally:
  exit