# (C) Ihsan Topcu - Ihsansoft - 2021
# This code is free to use.
# Pull requests are appreciated.

buttonPin = 26
API_KEY = "___API_KEY___"
Server = ""

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
    finally:
      GPIO.cleanup()
      exit
  
class CheckButton(Thread):
  def run(self):
    while True:
      if GPIO.input(buttonPin):
        print("Button pressed")
        contenttype = "Content-Type: application/json"
        request_on = json.dumps({"command":"turnPSUn"})
        request_off = json.dumps({"command":"turnPSUOff"})
        if (state == True):
          requests.post("http://" + Server + "/api/plugin/psucontrol", request_off, headers= {"X-Api-Key:"+ API_KEY: contenttype},)
        else:
          requests.post("http://" + Server + "/api/plugin/psucontrol", request_on, headers= {"X-Api-Key:"+ API_KEY: contenttype},)

try:
  GPIO.setmode(gpio.BCM)
  GPIO.setup(buttonPin, GPIO.IN)
  state = False
  event = threading.Event()
  ButtonThread = CheckButton()
  ApiThread = CheckAPI()
  print("Activating threads")
  ButtonThread.start()
  ApiThread.start()

except KeyboardInterrupt:
  print("\nEXIT")
finally:
  GPIO.cleanup()
  exit