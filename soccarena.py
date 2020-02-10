#!/usr/local/bin/python
'''
    File name: soccarena.py
    Author: Omar Faruki
    Date created: 02/04/2019
    Date last modified: 05/04/2019
    Python Version: 2.7
'''

#opening hours midweek:  14:00-22:30
#              Saturday: 10:00-22:00
#                Sunday: 10:00-21:00

import requests
from datetime import datetime
import collections

def printInfo(days_dict):
    if (not days_dict):
        print(":neverlucky:")
    else:
        for (day, court_dict) in sorted(days_dict.items()):
            if (not court_dict):
                continue
            day_of_week = datetime.strptime(day, '%d.%m.%Y').strftime('%A')
            print("")
            print(day_of_week + " " + day)
            for (court_name, slot_list) in sorted(court_dict.items()):
                if (len(slot_list) > 0):
                    print(court_name + ":")
                    for entry in slot_list:
                        print(entry)

def getFreeSlots(time_slots):
    free = False
    start_time = ""
    end_time = ""
    slots_list = []
    for (time, time_info) in time_slots.items():
        if ('label' in time_info):
            #slot is free
            if (not free):
                free = True
                start_time = time
        else:
            #slot is taken
            if (free and (day_of_week == "Saturday" or day_of_week == "Sunday")):
                free = False
                end_time = time
                timedelta = datetime.strptime(end_time, '%H:%M') - datetime.strptime(start_time, '%H:%M')
                if (timedelta.seconds/60 > 30):
                    slots_list.append(start_time + "-" + end_time)

            elif (free):
                free = False
                end_time = time
                timedelta = datetime.strptime(end_time, '%H:%M') - datetime.strptime(start_time, '%H:%M')
                if (int(end_time[:2]) >= 18 and timedelta.seconds/60 > 30):
                    slots_list.append(start_time + "-" + end_time)

    #check if last slot was free before moving on to the next court
    if (free and (day_of_week == "Saturday" or day_of_week == "Sunday")):
        free = False
        if (day_of_week == "Saturday"):
            end_time = "22:00"
        else:
            end_time = "21:00"
        timedelta = datetime.strptime(end_time, '%H:%M') - datetime.strptime(start_time, '%H:%M')
        if (timedelta.seconds/60 > 30):
            slots_list.append(start_time + "-" + end_time)
    elif (free):
        free = False
        end_time = "22:30"
        timedelta = datetime.strptime(end_time, '%H:%M') - datetime.strptime(start_time, '%H:%M')
        if (int(end_time[:2]) >= 18 and timedelta.seconds/60 > 30):
            slots_list.append(start_time + "-" + end_time)

    return slots_list

def getCourts(slots):
    courts_dict = dict()
    for (court, court_slots) in slots.items():
        if (int(court) == 5):
            match_court = "Speedcourt 4v4"
        else:
            match_court = "Match Court " + court
        time_slots = collections.OrderedDict(sorted(court_slots["slots"].items()))
        slots_list = getFreeSlots(time_slots)

        if (len(slots_list) > 0):
            courts_dict[match_court] = slots_list

    return courts_dict

def getAvailability(days):
    days_dict = dict()
    for (day, day_object) in days.items():
        global day_of_week
        day_of_week = datetime.strptime(day, '%d.%m.%Y').strftime('%A')
        holiday = day_object["holiday"]
        if (holiday):
            print(day_of_week + " is a holiday, SoccArena is closed!")
            continue
        slots = collections.OrderedDict(sorted(day_object["slots"].items()))
        courts_dict = getCourts(slots)
        days_dict[day] = courts_dict

    printInfo(days_dict)


print("Connecting to SoccArena Olympiapark...")
print("Reservation: https://www.soccarena-olympiapark.de/kalender.html")
print("Maps: https://goo.gl/maps/BxsigizN2A22")
print("")

response = requests.get('https://buchen.soccarena-olympiapark.de/frontend/calendar/rendering')
json_object = response.json()
days = collections.OrderedDict(sorted(json_object["days"].items()))
getAvailability(days)
