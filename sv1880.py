#!/usr/local/bin/python
'''
    File name: sv1880.py
    Author: Omar Faruki
    Date created: 04/04/2019
    Date last modified: 05/04/2019
    Python Version: 2.7
'''

#opening hours:  09:00-22:30

import requests
from datetime import datetime
from datetime import timedelta
import collections


print("Connecting to S.V.1880...")
print("Reservation: https://app.locaboo.com/de/booking/widget?user=1868")
print("Maps: https://goo.gl/maps/25aVxYw6Akp")
print("")
#acquire soccer-arena field id
field_locations = requests.post('https://app.locaboo.com/calendar/load_locations', json={"manager_id": "1868", "booking_mode": "true", "widget_mode": "true", "category": "", "locations": []})
location_id = 0
for location in field_locations.json()["cal_locations"]:
    if (location["name"] == "SOCCER-ARENA"):
        location_id = location["id"]
        break

#get field availabilities
current_date = datetime.today()
current_date_string = current_date.strftime('%Y-%m-%d')
date_in_a_week = current_date + timedelta(days=6)
date_in_a_week_string = date_in_a_week.strftime('%Y-%m-%d')
field_events = requests.post('https://app.locaboo.com/calendar/load_events', json={"date": current_date_string, "from": current_date_string, "to": date_in_a_week_string, "manager_id": "1868", "mode": "Week_single", "season_mode": "all", "widget": "true"})

days_dict = dict()
for event in field_events.json()["booked_locations"]:
    if (event["location_id"] == location_id):

        event_date = str(event["date"])
        event_start = str(event["from_hour"])
        event_end = str(event["to_hour"])
        if (event_date not in days_dict):
            days_dict[event_date] = [event_start + "-" + event_end]
        else:
            days_dict[event_date].append(event_start + "-" + event_end)

for (day, booked_slots) in sorted(days_dict.items()):
    closing_time = datetime.strptime('22:30', '%H:%M')
    day_of_week = datetime.strptime(day, '%Y-%m-%d').strftime('%A')
    modified_day = datetime.strptime(day, '%Y-%m-%d').strftime('%d.%m.%Y')
    if (day_of_week == "Saturday" or day_of_week == "Sunday"):
        current_time = datetime.strptime('09:00', '%H:%M')
    else:
        current_time = datetime.strptime('17:00', '%H:%M')
    print("\n" + day_of_week + " " + modified_day)
    for slot in booked_slots:
        split_slot = slot.split('-')
        slot_start_time = datetime.strptime(split_slot[0][:5], '%H:%M')
        slot_end_time = datetime.strptime(split_slot[1][:5], '%H:%M')
        if ((current_time < slot_start_time) and (slot_start_time - current_time).seconds/60 > 30):
            print(current_time.strftime('%H:%M') + "-" + slot_start_time.strftime('%H:%M'))

        current_time = slot_end_time
    if ((closing_time - current_time).seconds/60 > 30):
        print(current_time.strftime('%H:%M') + "-" + closing_time.strftime('%H:%M'))
