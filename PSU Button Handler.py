# (C) Ihsan Topcu - Ihsansoft - 2021
# This code is free to use.
# Pull requests are appreciated.

buttonPin = 26
API_KEY = "___API_KEY___"
Server = "localhost"

from json.decoder import JSONDecodeError
from requests import api
from requests.models import Response
from gpiozero import Button 
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
    global button
    while True:
      button.wait_for_press()
def switch():
  global state
  print("Button pressed")
  if (state == True):
    os.system("curl -s -H \"Content-Type: application/json\" -H \"X-Api-Key:"+ API_KEY +"\" -X POST -d '{ \"command\":\"turnPSUOff\" }\' -u username:password http://" + Server + "/api/plugin/psucontrol")
  else:
    os.system("curl -s -H \"Content-Type: application/json\" -H \"X-Api-Key:"+ API_KEY +"\" -X POST -d '{ \"command\":\"turnPSUOn\" }\' -u username:password http://" + Server + "/api/plugin/psucontrol")

try:
  state = False
  event = threading.Event()

  button = Button(buttonPin)
  ButtonThread = CheckButton()
  ApiThread = CheckAPI()
  button.when_pressed = switch
  print("Activating threads")
  ButtonThread.start()
  ApiThread.start()

except KeyboardInterrupt:
  print("\nEXIT")
finally:
  exit