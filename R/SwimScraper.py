import requests
import csv
from bs4 import BeautifulSoup as bs
import pandas as pd
import time as _time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

#sets path for chrome driver
executable_path = ChromeDriverManager().install()

teams = pd.read_csv('https://raw.githubusercontent.com/maflancer/SwimScraper/main/src/SwimScraper/collegeSwimmingTeams.csv')

events = {'25 Free' : 125, '25 Back' : 225, '25 Breast' : 325, '25 Fly' : 425, '50 Free' : 150, '75 Free' : 175, '100 Free' : 1100, '125 Free' : 1125, '200 Free' : 1200, '400 Free' : 1400, '500 Free' : 1500, '800 Free' : 1800, '1000 Free' : 11000, '1500 Free' : 11500, '1650 Free' : 11650, '50 Back' : 250, '100 Back': 2100, '200 Back' : 2200, '50 Breast' : 350, '100 Breast' : 3100, '200 Breast' : 3200, '50 Fly' : 450, '100 Fly' : 4100, '200 Fly' : 4200, '100 IM' : 5100, '200 IM' : 5200, '400 IM' : 5400, '200 Free Relay' : 6200, '400 Free Relay' : 6400, '800 Free Relay' : 6800, '200 Medley Relay' : 7200, '400 Medley Relay' : 7400, '1 M Diving' : 'H1', '3 M Diving' : 'H3', '7M Diving' : 'H75', 'Platform Diving' : 'H2', '50 Individual' : 'H50', '100 Individual' : 'H100', '200 Individual' : 'H200'}

us_states = {
	'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'District of Columbia': 'DC', 'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID',
	'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD', 'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO',
	'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK', 'Oregon': 'OR',
	'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV','Wisconsin': 'WI',
	'Wyoming': 'WY'
}

#HELPER FUNCTIONS -------------------------------------

#changes name from (last, first) to (first last)
def cleanName(webName):
	nameList = webName.split(', ')
	last_name = nameList[0]
	first_name = nameList[1]

	return first_name + ' ' +  last_name

#gets corresponding team number for a specified team
def getTeamID(team_name):
	team_number = -1

	#search for the specified team
	for index, row in teams.iterrows():
		if row['team_name'] == team_name:
			team_number = row['team_ID']
	return team_number

#gets corresponding team name for a specified team_ID
def getTeamName(team_ID):
    team_name = ''

    for index, row in teams.iterrows():
        if row['team_ID'] == team_ID:
            team_name = row['team_name']
    return team_name

#gets corresponding season ID for a specified year
def getSeasonID(year):
	return year - 1996

#gets corresponding year for a specified season_ID
def getYear(season_ID):
    return season_ID + 1996

def getEventName(event_ID):
    return list(events.keys())[list(events.values()).index(event_ID)]

def getEventID(event_name):
	return events.get(event_name)

#extracts state or country from hometown
def getState(hometown):
	home = hometown.split(',')[-1].strip()
	if(home.isalpha()):
		return home
	else:
		return 'NONE'

#extracts city from hometown
def getCity(hometown):
	home = hometown.split(',')
	home.pop() #removes state or country to isolate the city

	city = ' '.join([c.strip() for c in home])

	return city

#converts a time of the format minutes:seconds (1:53.8) to seconds (113.8)
def convertTime(display_time):
    if ':' in displayTime:
        timeArray = displayTime.split(':')
        seconds = float(timeArray[0]) * 60
        seconds += float(timeArray[1])

        return seconds
    elif displayTime.isalpha():
        pass
    else:
        return float(displayTime)

#for data from a html table (data), find the indexes where meet name, date, year, and improvement are
#returns an array [meet_name_index, date_index, imp_index]
def getIndexes(data):
	meet_name_index = -1
	date_index = -1
	imp_index = -1
	indexes = []

	i = 0
	for td in data:
		if td.has_attr('class') and td['class'][0] == 'hidden-xs':
			meet_name_index = i
		elif td.has_attr('class') and td['class'][0] == 'u-text-truncate':
			date_index = i
		elif td.has_attr('class') and td['class'][0] == 'u-text-end':
			imp_index = i

		i = i + 1

	indexes.append(meet_name_index)
	indexes.append(date_index)
	indexes.append(imp_index)

	return indexes


#SCRAPING FUNCTIONS ------------------------------------


#given a swimmer's ID, return their high school power index -> this is an index used for recruiting
#returns -1 if no swimmer found
def getPowerIndex(swimmer_ID):
	swimmer_url = 'https://swimcloud.com/swimmer/' + str(swimmer_ID)

	url = requests.get(swimmer_url, headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 'Referer' : 'https://google.com/'})

	url.encoding = 'utf-8'

	soup = bs(url.text, 'html.parser')

	data_array = soup.find_all('a', {'class' : 'c-list-bar__description'}) #this gets an array of 4 data points for the swimmer -> team, power_index, state rank, yearly rank

	try:
		return data_array[1].text.strip() #second element in the array is the swimmer's power index

	except IndexError: #there will be an indexError if no power index is found on the swimmer's page -> now, check an alternate page that may have the power index
		try:
			swimmer_name = soup.find('h1', {'class' : 'c-title'}).text.strip()

			swimmer_name_url = 'https://swimcloud.com/recruiting/rankings/?name=' + swimmer_name.replace(' ', '+')

			name_url = requests.get(swimmer_name_url, headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 'Referer' : 'https://google.com/'})

			name_url.encoding = 'utf-8'

			name_soup = bs(name_url.text, 'html.parser')

			swimmer_list = name_soup.find('tbody').find_all('tr')

			for swimmer in swimmer_list:
				#check if this is the correct swimmer using swimmer_ID
				id = swimmer.find_all('td')[1].find('a')['href'].split('/')[-1]
				if(int(id) == swimmer_ID):
					#a power index was found for the specified swimmer_ID!
					return name_soup.find('td', {'class' : 'u-text-end'}).text.strip()

			return -1 #if no swimmer is found with the correct swimmer ID #, return -1
		except IndexError: #if 0 swimmers show up on the page
			return -1

#takes as an input a swimmer's ID and returns a list of all events that they have participated in
def getSwimmerEvents(swimmer_ID):
	#set driver options
	chrome_options = Options()
	chrome_options.add_argument("--headless")
	driver = webdriver.Chrome(executable_path, options = chrome_options)
	ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)

	events = []
	swimmer_URL = 'https://www.swimcloud.com/swimmer/' + str(swimmer_ID) + '/'

	driver.get(swimmer_URL)

	tabs = driver.find_elements_by_css_selector('li.c-tabs__item')

	_time.sleep(1) #makes sure the event tab pops up on website

	for tab in tabs: #finds correct tab on swimmer's profile and clicks on it
		if(tab.text == 'Event'):
			tab.click()

	wait = WebDriverWait(driver, 10, ignored_exceptions = ignored_exceptions)

	try:
		event_dropdown = wait.until(EC.element_to_be_clickable((By.ID, 'byEventDropDownList'))) #waits for the event drop down list to show up
		event_dropdown.click()

		#find which events the swimmer has participated in
		html = driver.page_source
		soup = bs(html, 'html.parser')
		event_list = soup.find('ul', attrs = {'aria-labelledby' : 'byEventDropDownList'}).find_all('li')

		for event_li in event_list:
			events.append(event_li.text.strip())

	except TimeoutException: #if there are no events found for the swimmer
		return []

	driver.close()
	return events

#takes as an input a swimmer's ID # and returns a list of each indivudal time for the specified event
def getSwimmerTimes(swimmer_ID, event_name, event_ID = -1):
	#used chromedriver to interact with the swimcloud website and click on different dropdown menus

	#set driver options
	chrome_options = Options()
	chrome_options.add_argument("--headless")
	driver = webdriver.Chrome(executable_path, options = chrome_options)
	ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)

	time_list = list()
	if(event_ID == -1):
		event_ID = events.get(event_name)
	if(event_name == ''):
		event_name = getEventName(event_ID)
		#event_name = list(events.keys())[list(events.values()).index(event_ID)]

	swimmer_URL = 'https://www.swimcloud.com/swimmer/' + str(swimmer_ID) + '/'
	dropdownCheck = True
	eventCheck = True

	driver.get(swimmer_URL)

	tabs = driver.find_elements_by_css_selector('li.c-tabs__item')

	_time.sleep(1) #makes sure the event tab pops up on website

	for tab in tabs: #finds correct tab on swimmer's profile and clicks on it
		if(tab.text == 'Event'):
			tab.click()

	wait = WebDriverWait(driver, 10, ignored_exceptions = ignored_exceptions)

	try:
		event_dropdown = wait.until(EC.element_to_be_clickable((By.ID, 'byEventDropDownList'))) #waits for the event drop down list to show up
		event_dropdown.click()
	except TimeoutException: #if there is no event drop down
		dropdownCheck = False

	if dropdownCheck:

		swimmer_XPATH = '//a[@href="/swimmer/' + str(swimmer_ID)  + '/times/byevent/?event_id=' +  str(event_ID) + '"]'

		#print(swimmer_XPATH) #debug

		try:
			event = wait.until(EC.presence_of_element_located((By.XPATH, swimmer_XPATH)))
			event.click()
		except TimeoutException: #if a swimmer does not have the event listed in the dropdown
			eventCheck = False

		if eventCheck: #if the event is listed

			_time.sleep(1)

			html = driver.page_source

			soup = bs(html, 'html.parser')

			tables = soup.find_all('table', attrs = {'class' : 'c-table-clean'})
			i = 0

			#three different tables for the three pool types (LCM (long course meters), SCY (short course yards), SCM (long course meters))
			for table in tables:
				pool_type = table.find('caption').text.strip()

				try:
					times = tables[i].find_all('tr')[1:]
				except AttributeError:
					times = []

				for time in times:
					data = time.find_all('td')

					indexes = getIndexes(data) #this function finds the correct indexes for the meet name, date, year, and improvement, as they are different for some swimmers

					time = data[0].text.strip()

					if(indexes[0] == -1): #if no meet name was found
						meet = 'NA'
					else:
						meet = data[indexes[0]].text.strip()

					if(indexes[1] == -1): #if no date was found
						date = 'NA'
						year = 'NA'
					else:
						date = data[indexes[1]].text.strip()
						year = date.split(',')[-1]

					if(indexes[2] == -1): #if no imp was found
						imp = 'NA'
					else:
						imp = data[indexes[2]].text.strip()

					if(imp == '–'): #this character gets encoded weird in an excel doc so just set to NA
						imp = 'NA'

					time_list.append({'swimmer_ID' : swimmer_ID, 'pool_type' : pool_type, 'event': event_name, 'event_ID' : event_ID, 'time' : time, 'meet_name' : meet, 'year' : year, 'date' : date, 'improvement' : imp})

				i += 1

	driver.close()
	return time_list
