import pandas as pd
import sys
import csv
import string
import json
import urllib.request
import calendar


def finalPrint(year, weather, team1, team2, city1, city2, precip1, precip2, winner, percent):
	print('VERSION: 3 MONTHS')
	print('YEAR:', year)
	print('TYPE:', weather)
	print('TEAM-1:', team1)
	print('CITY-1:', city1)
	print('PRECIP-1:', precip1)	
	print('TEAM-2:', team2)
	print('CITY-2:', city2)
	print('PRECIP-2:', precip2)	
	print('WINNER:', winner)
	print('PERCENT: {}%'.format(percent))

userInput = sys.argv
team1 = userInput[1]
team2 = userInput[2]
year = userInput[3]
weather = userInput[4]
city1 = ''
city2 = ''
precip1 = 0.
precipWinner = 2.
precipLoser = 1.
precip2 = 0.
winner = ''
percent = 0

with open("NFL_data.csv", "r") as f:
	reader = csv.reader(f, delimiter="\t")	
	header = next(reader)
	for row in reader:
		#compare cities name with team input		
		teamName = row[0].split(",")[0]	
		if(teamName.lower().find(team1.lower()) != -1):		
			team1 = row[0].split(",")[0]
			city1 = row[0].split(",")[3][1:-1]


with open("NFL_data.csv", "r") as f:
	reader = csv.reader(f, delimiter="\t")	
	header = next(reader)
	for row in reader:
		#compare cities name with team input		
		teamName = row[0].split(",")[0]	
		if(teamName.lower().find(team2.lower()) != -1):			
			team2 = row[0].split(",")[0]
			city2 = row[0].split(",")[3][1:-1]	

if(city1 == ''):
	print("Team 1 not found")
	sys.exit()
if(city2 == ''):
	print("Team 2 not found")
	sys.exit()
if(weather.lower() != 'snow'):
	print('Incorrect Weather Input.')
	sys.exit()

month = 1
while(month <= 3):
	if(month == 2):
		if(calendar.isleap(int(year))):
			teamOneLink = "http://api.wunderground.com/api/40c38796d1d54db6/history_{}0{}29/q/{}.json".format(year, month, city1)
			teamTwoLink = "http://api.wunderground.com/api/40c38796d1d54db6/history_{}0{}29/q/{}.json".format(year, month, city2)	
		else:		
			teamOneLink = "http://api.wunderground.com/api/40c38796d1d54db6/history_{}0{}28/q/{}.json".format(year, month, city1)
			teamTwoLink = "http://api.wunderground.com/api/40c38796d1d54db6/history_{}0{}28/q/{}.json".format(year, month, city2)
	else:
		teamOneLink = "http://api.wunderground.com/api/40c38796d1d54db6/history_{}0{}31/q/{}.json".format(year, month, city1)
		teamTwoLink = "http://api.wunderground.com/api/40c38796d1d54db6/history_{}0{}31/q/{}.json".format(year, month, city2)

	month = month + 1

	request1 = urllib.request.Request(teamOneLink)
	response1 = urllib.request.urlopen(request1)
	json_string1 = response1.read().decode('utf-8')
	parsed_json1 = json.loads(json_string1)
	temp1 = parsed_json1['history']['dailysummary'][0]['monthtodatesnowfalli']
	if(temp1 == '' or temp1 == 'T'):
		temp1 = 0
	precip1 = precip1 + float(temp1)

	request2 = urllib.request.Request(teamTwoLink)
	response2 = urllib.request.urlopen(request2)
	json_string2 = response2.read().decode('utf-8')
	parsed_json2 = json.loads(json_string2)
	temp2 = parsed_json2['history']['dailysummary'][0]['monthtodatesnowfalli']
	if(temp2 == '' or temp2 == 'T'):
		temp2 = 0
	precip2 = precip2 + float(temp2)

if(precip1 > precip2):
	winner = team1
	precipWinner = precip1
	precipLoser = precip2
elif(precip2 > precip1):
	precipWinner = precip2
	precipLoser = precip1
	winner = team2
else:
	precipWinner = precip1
	precipLoser = precip2
	winner = 'No Winner'
if(precipLoser == 0 and winner != 'No Winner'):
	percent = 'Infinity'
elif(precipLoser == 0 and winner == 'No Winner'):
	percent = ''
else:
	percent = 100 * ((precipWinner/precipLoser) - 1)
finalPrint(year, weather, team1, team2, city1, city2, precip1, precip2, winner, percent)