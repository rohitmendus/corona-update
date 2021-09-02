from tkinter import *
from tkinter import messagebox
import requests
import json
import pyttsx3
# import re
import threading

class web_scrape:
	def __init__(self):
		self.auth=("covid19-pro", "e2RQj7zEJj##4n<v")
		self.api = requests.get('https://api.covid19api.com/summary', auth=self.auth)
		self.data = json.loads(self.api.text)


	def get_total(self, argument):
		if argument == "cases":
			return self.data['Global']['TotalConfirmed']
		elif argument == "deaths":
			return self.data['Global']['TotalDeaths']
		elif argument == "new_cases":
			return self.data['Global']['NewConfirmed']
		elif argument == "new_deaths":
			return self.data['Global']['NewDeaths']


class VoiceAssistant:
	def __init__(self):
		self.engine = pyttsx3.init()
		rate = self.engine.getProperty('rate')
		self.engine.setProperty('rate', rate-30)
		voices = self.engine.getProperty('voices')
		self.engine.setProperty('voice', voices[1].id)

	def speak(self, text):
		self.engine.say(text)
		self.engine.runAndWait() 


class App:
	def __init__(self, master, scraper, voice):
		self.master = master
		self.master.iconbitmap('virus.ico')
		self.master.title("Corona Updater")
		self.master.maxsize('864', '564')
		self.master.minsize('864', '564')
		self.master.configure(bg="#eb4034")
		self.scraper = scraper
		self.voice = voice
		updating = threading.Thread(target=self.update)
		updating.start()
		self.master.mainloop()

	def update(self):
		total_cases = self.scraper.get_total("cases")
		new_cases = self.scraper.get_total("new_cases")
		total_deaths = self.scraper.get_total("deaths")
		new_deaths = self.scraper.get_total("new_deaths")
		speech = f'''Good Day!....
		There have been {new_cases} new cases reported adding up to a total of {total_cases} cases.
		{new_deaths} deaths have aslo been reported which has added up to a total of {total_deaths} deaths.
		To get results of more a specic region, enter the country name in the field!'''
		self.voice.speak(speech)



window = Tk()
scraper = web_scrape()
voice = VoiceAssistant()
app = App(window, scraper, voice)

