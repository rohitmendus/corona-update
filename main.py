import requests
import json
import pyttsx3
import re

class Data:
	def __init__(self):
		self.api = requests.get('https://api.covid19api.com/summary')



class gui:
	def __init__(self, master):
		self.master = master


# data = json.loads(corona_api.text)
# print(data)
# print(data["Global"]["TotalConfirmed"])
# engine = pyttsx3.init()
# engine.say("Hello there! Whatsupp")
# engine.runAndWait() 
