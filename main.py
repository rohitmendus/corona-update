from tkinter import *
from tkinter import messagebox, ttk, font
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
			if country.lower().find(i['Country'].lower()) != -1:
				data['country'] = i["Country"]
				data['cases'] = i["TotalConfirmed"]
				data['deaths'] = i["TotalDeaths"]
				data['new_cases'] = i["NewConfirmed"]
				data["new_deaths"] = i["NewDeaths"]
		return data


	def get_country(self):
		countries = []
		for i in self.data["Countries"]:
			countries.append(i["Country"])
		return countries


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
		while True:    
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
		self.master = master
		self.bg_color = "#eb4034"
		print(self.scraper.get_country_data("hello hello IndIa hello"))
		self.master.iconbitmap('virus.ico')
		self.master.title("Corona Updater")
		self.master.maxsize('864', '664')
		self.master.minsize('864', '664')
		self.master.configure(bg=self.bg_color)
		self.master.protocol("WM_DELETE_WINDOW", self.exit)
		self.update()
		self.master.mainloop()


	def clear(self):
		lis = self.master.winfo_children()
		for i in lis:
			i.destroy()


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
		self.updating = threading.Thread(target=self.latest_news)
		self.updating.start()
		self.set_up()


	def latest_news(self):
		speech = f'''Good Day!....
		There have been {self.new_cases} new cases reported adding up to a total of {self.total_cases} cases.
		{self.new_deaths} deaths have also been reported which has added up to a total of {self.total_deaths} deaths.'''
		# self.voice.speak(speech)


	def ask(self):
		self.ask_btn.config(text="Listening", state="disabled")
		text = self.voice.listen()
		print(text)
		data1 = self.scraper.get_country_data(text)
		if bool(data1):
			if text.find("new") != -1 and text.find("cases") != -1:
				value = "{:,}".format(data1["new_case"])
				country = data1["country"]
				self.voice.speak(f"There are {value} new cases in {country}")
			elif text.find("case") != -1:
				value = "{:,}".format(data1["cases"])
				country = data1["country"]
				self.voice.speak(f"There are a total number of {value} cases in {country}")
			elif text.find("new") != -1 and text.find("death") != -1:
				value = "{:,}".format(data1["new_deaths"])
				country = data1["country"]
				self.voice.speak(f"There are {value} new deaths in {country}")
			elif text.find("death") != -1:
				value = "{:,}".format(data1["deaths"])
				country = data1["country"]
				self.voice.speak(f"There are a total number of {value} deaths so far in {country}")
			else:
				value_1 = "{:,}".format(data1["cases"])
				value_2 = "{:,}".format(data1["new_cases"])
				value_3 = "{:,}".format(data1["deaths"])
				value_4 = value = "{:,}".format(data1["new_deaths"])
				country = data1["country"]
				self.voice.speak(f"""There are {value_2} new cases in {country} adding to a total of {value_1} cases.
					{value_4} new deaths have also been reported adding to the total of {value_3} deaths.""")
		else:
			pass
		self.ask_btn.config(text="Ask", state="normal")


	def country_news(self, i):
		print(i)


	def set_up(self):
		self.clear()
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
		self.update_btn = Button(self.master, text="Update", activebackground="green", activeforeground="white", font=('Helvetica', 16), width = 10, bg="green", fg="white", command=self.update)
		self.update_btn.place(x=380, y=280)
		self.ask_btn = Button(self.master, text="Ask", activebackground="blue", activeforeground="white", font=('Helvetica', 16), width = 10, bg="blue", fg="white", command=lambda: threading.Thread(target=self.ask).start())
		self.ask_btn.place(x=380, y=600)
		myfont = font.Font(family="Helvetica",size=16)
		self.master.option_add("*TCombobox*Listbox*Font", myfont)
		self.sel_country = ttk.Combobox(self.master, font=('Helvetica', 16))
		self.sel_country["values"] = tuple(self.scraper.get_country())
		self.sel_country.bind("<<ComboboxSelected>>", self.country_news)
		self.sel_country.place(x=300, y=350)


if __name__ == '__main__':	
	window = Tk()
	scraper = web_scrape()
	voice = VoiceAssistant()
	app = App(window, scraper, voice)

