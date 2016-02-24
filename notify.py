# Get data from MTA
import urllib, json, re
from pprint import pprint
import datetime
import math
import dateutil.parser, pytz

def minutes_left(arrival):
	now = datetime.datetime.now(pytz.timezone('US/Eastern'))
	diff = arrival - now
	if diff.seconds < 20:
		diff = 0
	if diff.seconds > 1000 * 60:
		diff = 0
	return int(math.ceil(diff.seconds / 60))

def next_arrival():
	url = "http://api.wheresthefuckingtrain.com/by-id/367"
	response = urllib.urlopen(url)
	data = json.loads(response.read())
	arrivals = data["data"][0]['S']
	first_two_arrivals = arrivals[:2]
	for arrival in arrivals:
		arrival['time'] = dateutil.parser.parse(arrival['time'])
		arrival['mins_until'] = minutes_left(arrival['time'])
	texts = ["(%s) South Ferry - %d min" % (arrival['route'], arrival['mins_until']) for arrival in arrivals]
	next_train = texts[0]
	return next_train

# Print to DotHat
import dothat.lcd as lcd
import dothat.backlight as backlight

def tidyup():
    backlight.off()
    backlight.set_graph(0)
    lcd.clear()

def turn_on_backlight():
	r=100
	g=100
	b=100
	backlight.rgb(r,g,b)

if __name__ == "__main__":
	turn_on_backlight()
	text_to_display = next_arrival

	while True:
		if text_to_display != next_arrival:
			lcd.clear()
			lcd.write("145 st ")
			lcd.write(next_arrival)
			text_to_display = next_arrival
		time.sleep(10)
