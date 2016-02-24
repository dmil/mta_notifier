import dothat.lcd as lcd
import dothat.backlight as backlight

lcd.write('test')
backlight.off()

import urllib, json, re

url = "http://mtaapi.herokuapp.com/api?id=114S"
response = urllib.urlopen(url)
data = json.loads(response.read())
arrivals = data["result"]["arrivals"]

import time

arrival_times = []
for arrival in arrivals:
	hour = arrival[0:2]
	if hour == "24":
		arrival = "00" + arrival[2:] 
	t = time.strptime(arrival,"%H:%M:%S")
	arrival_times.append(arrivals)

arrival_times = sorted(arrival_times)
arrival_times = [arrival_time for arrival_time in arrival_times if arrival_time > time.time()]
print arrival_times




