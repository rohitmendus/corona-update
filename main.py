from tkinter import *
from tkinter import messagebox
import requests
import json
import pyttsx3
import re
import speech_recognition as sr
import threading

class web_scrape:
	def __init__(self):
		self.auth=("covid19-pro", "e2RQj7zEJj##4n<v")
		self.api = requests.get('https://api.covid19api.com/summary', auth=self.auth)
		self.data = json.loads(self.api.text)
		# print(self.data)


	def update_data(self):
		self.auth=("covid19-pro", "e2RQj7zEJj##4n<v")
		self.api = requests.get('https://api.covid19api.com/summary', auth=self.auth)
		self.data = json.loads(self.api.text)


	def get_total(self, argument):
		if argument == "cases":
			total_cases = self.data['Global']['TotalConfirmed']
			total_cases = "{:,}".format(total_cases)
			return total_cases
		elif argument == "deaths":
			total_deaths = self.data['Global']['TotalDeaths']
			total_deaths = "{:,}".format(total_deaths)
			return total_deaths
		elif argument == "new_cases":
			new_cases = self.data['Global']['NewConfirmed']
			new_cases = "{:,}".format(new_cases)
			return new_cases
		elif argument == "new_deaths":
			new_deaths = self.data['Global']['NewDeaths']
			new_deaths = "{:,}".format(new_deaths)
			return new_deaths

	def get_country_data(self, country):
		data = {}
		for i in self.data['Countries']:
			if i['Country'].lower() == country.lower():
				data['cases'] = i["TotalConfirmed"]
				data['deaths'] = i["TotalDeaths"]
				data['new_cases'] = i["NewConfirmed"]
				data["new_deaths"] = i["NewDeaths"]
		return data



class VoiceAssistant:
	def __init__(self):
		self.engine = pyttsx3.init()
		rate = self.engine.getProperty('rate')
		self.engine.setProperty('rate', rate-30)
		voices = self.engine.getProperty('voices')
		self.engine.setProperty('voice', voices[1].id)
		self.r = sr.Recognizer() 

	def speak(self, text):
		self.engine.say(text)
		self.engine.runAndWait()


	def listen(self):
		while(1):    
		    try:
		        with sr.Microphone() as source2:
		            self.r.adjust_for_ambient_noise(source2, duration=0.2)
		            audio2 = self.r.listen(source2)
		            text = self.r.recognize_google(audio2)
		            text = text.lower()
		            return text
		              
		    except sr.RequestError as e:
		        print("Could not request results; {0}".format(e))
		          
		    except sr.UnknownValueError:
		        print("unknown error occured") 


class App:
	def __init__(self, master, scraper, voice):
		self.scraper = scraper
		self.voice = voice
		self.update()
		self.master = master
		self.bg_color = "#eb4034"
		self.master.iconbitmap('virus.ico')
		self.master.title("Corona Updater")
		self.master.maxsize('864', '664')
		self.master.minsize('864', '664')
		self.master.configure(bg=self.bg_color)
		self.master.protocol("WM_DELETE_WINDOW", self.exit)
		updating = threading.Thread(target=self.latest_news)
		updating.start()
		self.set_up()
		self.master.mainloop()

	def exit(self):
		ask = messagebox.askyesno("Exit", "Are you sure that you want to exit?")
		if ask == 1:
			self.master.destroy()

	def update(self):
		self.scraper.update_data()
		self.total_cases = self.scraper.get_total("cases")
		self.new_cases = self.scraper.get_total("new_cases")
		self.total_deaths = self.scraper.get_total("deaths")
		self.new_deaths = self.scraper.get_total("new_deaths")

	def latest_news(self):
		speech = f'''Good Day!....
		There have been {self.new_cases} new cases reported adding up to a total of {self.total_cases} cases.
		{self.new_deaths} deaths have also been reported which has added up to a total of {self.total_deaths} deaths.'''
		self.voice.speak(speech)


	def set_up(self):
		self.main_figures_frame = Frame(self.master, bg=self.bg_color)
		self.tot_cases_lab_num = Label(self.main_figures_frame, text=self.total_cases, font=('Helvetica', 36), fg="white", bg=self.bg_color)
		self.tot_cases_lab = Label(self.main_figures_frame, text="cases", font=('Helvetica', 20), fg="white", bg=self.bg_color)
		self.new_cases_lab_num = Label(self.main_figures_frame, text=self.new_cases, font=('Helvetica', 36), fg="white", bg=self.bg_color)
		self.new_cases_lab = Label(self.main_figures_frame, text="new cases", font=('Helvetica', 20), fg="white", bg=self.bg_color)
		self.tot_deaths_lab_num = Label(self.main_figures_frame, text=self.total_deaths, font=('Helvetica', 36), fg="white", bg=self.bg_color)
		self.tot_deaths_lab = Label(self.main_figures_frame, text="deaths", font=('Helvetica', 20), fg="white", bg=self.bg_color)
		self.new_deaths_lab_num = Label(self.main_figures_frame, text=self.new_deaths, font=('Helvetica', 36), fg="white", bg=self.bg_color)
		self.new_deaths_lab = Label(self.main_figures_frame, text="new deaths", font=('Helvetica', 20), fg="white", bg=self.bg_color)
		self.main_figures_frame.place(x=50, y=30)
		self.tot_cases_lab_num.grid(row=0, column=0, padx=65)
		self.tot_cases_lab.grid(row=1, column=0, padx=65)
		self.tot_deaths_lab_num.grid(row=0, column=1, padx=65)
		self.tot_deaths_lab.grid(row=1, column=1, padx=65)
		self.new_cases_lab_num.grid(row=2, column=0, padx=65, pady=(30, 0))
		self.new_cases_lab.grid(row=3, column=0, padx=65)
		self.new_deaths_lab_num.grid(row=2, column=1, padx=65, pady=(30, 0))
		self.new_deaths_lab.grid(row=3, column=1, padx=65)


if __name__ == '__main__':	
	window = Tk()
	scraper = web_scrape()
	voice = VoiceAssistant()
	app = App(window, scraper, voice)

