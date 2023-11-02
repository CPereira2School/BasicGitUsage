import requests
import json #Part of requests I guess?
import datetime
from colorama import init, Fore, Style
init()

"""
Listing the stops
"""

API_KEY = "ymFOhCrlE6EHgrazuY8x"
lon = -97.08002481349236 # Flying Pizza on Edison
lat = 49.938127673372634
distance = 100

url_stops = f"https://api.winnipegtransit.com/v3/stops.json?lon={lon}&lat={lat}&distance={distance}&api-key={API_KEY}"

response = requests.get(url_stops).json()

stopList = response['stops']

print(f"Stops available within {distance} from coordinates ({lon}, {lat})")

for stop in stopList:
  print(f"  {stop['key']} {stop['name']}")

"""
Taking user input and listing schedule(s)
"""

print(f"Enter stop number: ")

enteredValue = input()

# Looping through the stop list to  find the user submitted stop

url_schedules = f"https://api.winnipegtransit.com/v3/stops/{enteredValue}/schedule.json?max-results-per-route=2&api-key={API_KEY}"

response2 = requests.get(url_schedules).json()

scheduleList = response2['stop-schedule']

# Looping through the schedule API json data
for routeSchedule in scheduleList['route-schedules']:
    for scheduledStop in routeSchedule['scheduled-stops']:
        times = scheduledStop['times']
        scheduledTime = datetime.datetime.fromisoformat(times['departure']['scheduled'])
        formattedScheduledTime = scheduledTime.strftime("%H:%M:%S")
        estimatedTime = datetime.datetime.fromisoformat(times['departure']['estimated'])
        formattedEstimatedTime = estimatedTime.strftime("%H:%M:%S")
        if scheduledTime < estimatedTime:
           color = Fore.RED
        elif scheduledTime > estimatedTime:
           color = Fore.BLUE
        if scheduledTime == estimatedTime:
           color = Fore.GREEN

        print(f"  {color}Scheduled: {formattedScheduledTime}{Style.RESET_ALL}   {color}Estimated: {formattedEstimatedTime}{Style.RESET_ALL}")

'''
Old and much easier to read version of my loop code, lol

for routeSchedule in scheduleList['route-schedules']:
    for scheduledStop in routeSchedule['scheduled-stops']:
        times = scheduledStop['times']
        print(f"  Scheduled: {times['departure']['scheduled']}   Estimated: {times['departure']['estimated']}")

'''

'''
This block of code was a failed attempt at error handling. The expectation in this assignment is that the user will submit a valid entry, so this can be ignored.

correctInput = False

for stop in stopList:
  if int(stop['key']) != int(enteredValue):
    correctInput = True
    break

if correctInput == False:
  print(f"No stop within {distance} has that stop number.")
  exit() # NOT WORKING NICELY :('''