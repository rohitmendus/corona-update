# Importing necessary modules
from tkinter import *
from tkinter import messagebox, ttk, font
import requests
import json
import pyttsx3
import speech_recognition as sr
import threading

# This class scrapes the required data from an API response
class web_scrape:
	# Gets the data from the API response
	def update_data(self):
		self.auth=("covid19-pro", "e2RQj7zEJj##4n<v")
		self.api = requests.get('https://api.covid19api.com/summary', auth=self.auth)
		self.data = json.loads(self.api.text)


	# Gets the data for the overall cases and deaths
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


	#Gets the data regarding a specific country(cases, deaths, new cases and new deaths)
	def get_country_data(self, country):
		data = {}
		if country.find("america") != -1 or country.find("usa") != -1:
			for i in self.data['Countries']:
				if i['Country'] == "United States of America":
					data['country'] = i["Country"]
					data['cases'] = i["TotalConfirmed"]
					data['deaths'] = i["TotalDeaths"]
					data['new_cases'] = i["NewConfirmed"]
					data["new_deaths"] = i["NewDeaths"]
		else:
			for i in self.data['Countries']:
				if country.lower().find(i['Country'].lower()) != -1:
					data['country'] = i["Country"]
					data['cases'] = i["TotalConfirmed"]
					data['deaths'] = i["TotalDeaths"]
					data['new_cases'] = i["NewConfirmed"]
					data["new_deaths"] = i["NewDeaths"]
		return data


	#Gets the list of countries
	def get_country(self):
		countries = []
		for i in self.data["Countries"]:
			countries.append(i["Country"])
		return countries


# This class is responsible for all the speech and listening of the application.
class VoiceAssistant:
	def __init__(self):
		# Initialising the pyttsx3 speech engine
		self.engine = pyttsx3.init()
		# Addding characteristic properties to the sound 
		rate = self.engine.getProperty('rate')
		self.engine.setProperty('rate', rate-30)
		voices = self.engine.getProperty('voices')
		self.engine.setProperty('voice', voices[1].id)
		# Setting up the speech recogniser
		self.r = sr.Recognizer()

	# Speaks a given text
	def speak(self, text):
		self.engine.say(text)
		self.engine.runAndWait()


	# Listens to the user and returns the text
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


# Class for the main application. 
# Brings the above two classes together as well as sets up the GUI enironment.
class App:
	def __init__(self, master, scraper, voice):
		# Initialises the scraper, voice and GUI window.
		self.scraper = scraper
		self.voice = voice
		self.master = master
		# Defines the properties of the window
		self.bg_color = "#eb4034"
		self.master.iconbitmap('virus.ico')
		self.master.title("Corona Updater")
		self.master.maxsize('864', '664')
		self.master.minsize('864', '664')
		self.master.configure(bg=self.bg_color)
		# Exit protocol
		self.master.protocol("WM_DELETE_WINDOW", self.exit)
		# Updates the data
		self.update()
		# Runs the mainloop
		self.master.mainloop()

	# Clears the GUI window
	def clear(self):
		lis = self.master.winfo_children()
		for i in lis:
			i.destroy()

	# Asking for confirmation to exit
	def exit(self):
		ask = messagebox.askyesno("Exit", "Are you sure that you want to exit?")
		if ask == 1:
			self.master.destroy()

	# Gets the data from the scraper and runs a news broadcast
	def update(self):
		# Getting data....
		self.scraper.update_data()
		self.total_cases = self.scraper.get_total("cases")
		self.new_cases = self.scraper.get_total("new_cases")
		self.total_deaths = self.scraper.get_total("deaths")
		self.new_deaths = self.scraper.get_total("new_deaths")
		# Starting the thread for the lates COVID-19 news.
		self.updating = threading.Thread(target=self.latest_news)
		self.updating.start()
		#Settig up the Tkinter widgets
		self.set_up()


	# Speeks about the lates news
	def latest_news(self):
		speech = f'''Good Day!....
		There have been {self.new_cases} new cases reported adding up to a total of {self.total_cases} cases.
		{self.new_deaths} deaths have also been reported which has added up to a total of {self.total_deaths} deaths.'''
		self.voice.speak(speech)


	# Gets data about the country when user asks.
	def ask(self):
		self.ask_btn.config(text="Listening", state="disabled")
		# Gets the text from the user via recognizer
		text = self.voice.listen()
		# Scrapes for country data
		data1 = self.scraper.get_country_data(text)
		# This statement checks if the country was valid or not
		if bool(data1):
			# If valid then gets to work for a reply
			self.country_news(country = data1["country"])
			if text.find("new") != -1 and text.find("case") != -1:
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
		# The rest of the elif statement works to check if the user meant the overall data
		elif text.find("new") != -1 and text.find("case") != -1:
			self.voice.speak(f"There are {self.new_cases} new cases.")
		elif text.find("case") != -1:
			self.voice.speak(f"There are a total number of {self.total_cases} cases.")
		elif text.find("new") != -1 and text.find("death") != -1:
			self.voice.speak(f"There are {self.new_deaths} new deaths.")
		elif text.find("death") != -1:
			self.voice.speak(f"There are a total number of {self.total_deaths} deaths so far.")
		elif text.find("covid") != -1 or text.find("corona") != -1:
			speech = f'''There have been {self.new_cases} new cases reported adding up to a total of {self.total_cases} cases.
						{self.new_deaths} deaths have also been reported which has added up to a total of {self.total_deaths} deaths.'''
			self.voice.speak(speech)
		# If the statements above wasn't able to find what the user meant or if the user asked for irrelevant information
		else:
			self.voice.speak("Sorry can't find what you are looking for!")
		# Changes the state of ask button to normal
		self.ask_btn.config(text="Ask", state="normal")


	# Gets the news about a particular country on the GUI screen
	def country_news(self, i=None, country=None):
		if country != None:
			pass
		else:
			country = self.sel_country.get().lower()
		self.sel_country.set(country.title())
		data = self.scraper.get_country_data(country)
		if bool(data):
			self.cnt_tot_cases_lab_num.config(text="{:,}".format(data["cases"]))
			self.cnt_tot_deaths_lab_num.config(text="{:,}".format(data["deaths"]))
			self.cnt_new_cases_lab_num.config(text="{:,}".format(data["new_cases"]))
			self.cnt_new_deaths_lab_num.config(text="{:,}".format(data["new_deaths"]))
		else:
			pass


	# Sets up the widgets for the main window
	def set_up(self):
		self.clear()
		# Creating widgets for displaying the main figures
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
		# The update btn redirects to the self.update() function 
		self.update_btn = Button(self.master, text="Update", activebackground="green", activeforeground="white", font=('Helvetica', 16), width = 10, bg="green", fg="white", command=self.update)
		self.update_btn.place(x=380, y=280)
		# The ask_btn redirects to the self.ask() function
		self.ask_btn = Button(self.master, text="Ask", activebackground="blue", activeforeground="white", font=('Helvetica', 16), width = 10, bg="blue", fg="white", command=lambda: threading.Thread(target=self.ask).start())
		self.ask_btn.place(x=380, y=600)
		# Making the font size of the combobox to be the same
		myfont = font.Font(family="Helvetica",size=16)
		# Changes font of the listbox in combobox
		self.master.option_add("*TCombobox*Listbox*Font", myfont)
		self.sel_country = ttk.Combobox(self.master, font=('Helvetica', 16))
		self.sel_country["values"] = tuple(self.scraper.get_country())
		# If an item inside the combox is selected it redirects to the self.country_news() function
		self.sel_country.bind("<<ComboboxSelected>>", self.country_news)
		self.sel_country.place(x=300, y=350)
		# The search btn redirects to the self.country_news() function
		# It is for displaying results on the search in the combobox
		self.srch_btn = Button(self.master, text="Search", activebackground="green", activeforeground="white", font=('Helvetica', 16), width = 10, bg="green", fg="white", command=self.country_news)
		self.srch_btn.place(x=600, y=350)
		# Setting up of widgets for the country data
		self.country_figures_frame = Frame(self.master, bg=self.bg_color)
		self.cnt_tot_cases_lab_num = Label(self.country_figures_frame, text="", font=('Helvetica', 20), fg="white", bg=self.bg_color)
		self.cnt_tot_cases_lab = Label(self.country_figures_frame, text="cases", font=('Helvetica', 16), fg="white", bg=self.bg_color)
		self.cnt_new_cases_lab_num = Label(self.country_figures_frame, text="", font=('Helvetica', 20), fg="white", bg=self.bg_color)
		self.cnt_new_cases_lab = Label(self.country_figures_frame, text="new cases", font=('Helvetica', 16), fg="white", bg=self.bg_color)
		self.cnt_tot_deaths_lab_num = Label(self.country_figures_frame, text="", font=('Helvetica', 20), fg="white", bg=self.bg_color)
		self.cnt_tot_deaths_lab = Label(self.country_figures_frame, text="deaths", font=('Helvetica', 16), fg="white", bg=self.bg_color)
		self.cnt_new_deaths_lab_num = Label(self.country_figures_frame, text="", font=('Helvetica', 20), fg="white", bg=self.bg_color)
		self.cnt_new_deaths_lab = Label(self.country_figures_frame, text="new deaths", font=('Helvetica', 16), fg="white", bg=self.bg_color)
		self.cnt_tot_cases_lab_num.grid(row=0, column=0, padx=65)
		self.cnt_tot_cases_lab.grid(row=1, column=0, padx=65)
		self.cnt_tot_deaths_lab_num.grid(row=0, column=1, padx=65)
		self.cnt_tot_deaths_lab.grid(row=1, column=1, padx=65)
		self.cnt_new_cases_lab_num.grid(row=2, column=0, padx=65, pady=(30, 0))
		self.cnt_new_cases_lab.grid(row=3, column=0, padx=65)
		self.cnt_new_deaths_lab_num.grid(row=2, column=1, padx=65, pady=(30, 0))
		self.cnt_new_deaths_lab.grid(row=3, column=1, padx=65)
		self.country_figures_frame.place(x=200, y = 400)


# Runs the application
if __name__ == '__main__':	
	window = Tk()
	scraper = web_scrape()
	voice = VoiceAssistant()
	app = App(window, scraper, voice)

