# Get data from MTA
import urllib, json, re
from pprint import pprint
import datetime
import math
import dateutil.parser, pytz


url = "http://api.wheresthefuckingtrain.com/by-id/367"
response = urllib.urlopen(url)
data = json.loads(response.read())
arrivals = data["data"][0]['S']
first_two_arrivals = arrivals[:2]

def minutes_left(arrival):
	now = datetime.datetime.now(pytz.timezone('US/Eastern'))
	diff = arrival - now
	if diff.seconds < 20:
		diff = 0
	return int(math.ceil(diff.seconds / 60))


for arrival in arrivals:
	arrival['time'] = dateutil.parser.parse(arrival['time'])
	arrival['mins_until'] = minutes_left(arrival['time'])

texts = ["(%s) South Ferry - %d min" % (arrival['route'], arrival['mins_until']) for arrival in arrivals]
next_train = texts[0]
print next_train

# Print to DotHat
# import dothat.lcd as lcd
# import dothat.backlight as backlight

# lcd.write('test')
# backlight.off()
