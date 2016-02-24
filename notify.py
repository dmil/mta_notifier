# Get data from MTA
import urllib, json, re
from pprint import pprint
import datetime, time
import math
import dateutil.parser, pytz

def minutes_left(arrival):
	now = datetime.datetime.now(pytz.timezone('US/Eastern'))
	diff = arrival - now
	if diff.seconds < 20:
		return 0
	if diff.seconds > 1000 * 60:
		return 0
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
	return arrivals[0]

# Print to DotHat
# import dothat.lcd as lcd
# import dothat.backlight as backlight

def tidyup():
    backlight.off()
    backlight.set_graph(0)
    lcd.clear()

def write_lines(line1, line2, line3):
	if len(line1) > 16 or len(line2) > 16 or len(line3) > 16:
		raise

	lcd.set_cursor_position(0,0)
	lcd.write(line1)
	lcd.set_cursor_position(0,1)
	lcd.write(line2)
	lcd.set_cursor_position(0,2)
	lcd.write(line3)

def write_minutes(mins):
	write_lines(
		"145 st",
		"(1) South Ferry",
		" -- %d min -- " % mins
	)

def turn_on_backlight():
	r=100
	g=100
	b=100
	backlight.rgb(r,g,b)

if __name__ == "__main__":
	turn_on_backlight()
	mins_till_train = next_arrival()['mins_until']
	lcd.clear()
	write_minutes(mins_till_train)

	while True:
		if mins_till_train != next_arrival()['mins_until']:
			print "new time found"
			lcd.clear()
			mins_till_train = next_arrival()['mins_until']
			write_minutes(mins_till_train)
		else:
			print "new time not found"
		time.sleep(10)
