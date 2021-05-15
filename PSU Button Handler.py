# (C) Ihsan Topcu - Ihsansoft - 2021
# This code is free to use.
# Pull requests are appreciated.

buttonPin = 17
API_KEY = "___API_KEY___"
Server = "localhost"

import RPi.GPIO as GPIO
import time
import requests
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
        event.wait(2)
    except ConnectionRefusedError:
      print("Connection refused")
    except ConnectionError:
      print("Connection error")
    except KeyError:
      print("KeyError: Is the API Key correct?")

def checkbtn():
  inputbtn = GPIO.input(buttonPin)
  print(inputbtn)
  if inputbtn == 1:
    return 1
  else:
    return 0

class CheckButton(Thread):
  def run(self):
    while True:
      if checkbtn() == 1:
        print("Button pressed")
        request_on = json.dumps({"command":"turnPSUOn"})
        request_off = json.dumps({"command":"turnPSUOff"})
        if (state == True):
          requests.post("http://" + Server + "/api/plugin/psucontrol", data=request_off, headers= {"X-Api-Key" : API_KEY, "Content-Type" : "application/json"})
        else:
          requests.post("http://" + Server + "/api/plugin/psucontrol", data=request_on, headers= {"X-Api-Key" : API_KEY, "Content-Type" : "application/json"})

try:
  state = False
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(buttonPin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
  event = threading.Event()
  ButtonThread = CheckButton()
  ApiThread = CheckAPI()
  print("Activating threads")
  ApiThread.start()
  ButtonThread.start()


except KeyboardInterrupt:
  print("\nEXIT")