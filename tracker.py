#!/usr/bin/env python

import re
import requests
import json
import math
from bs4 import BeautifulSoup

location 	= raw_input("Enter your address [Blank to use ip address] ")

if location == '':
	loc	= requests.get("http://freegeoip.net/json/").text.strip()
	loc	= json.loads(loc)
	lat	= loc['latitude']
	lon	= loc['longitude']
else:
	url 	= 'https://maps.googleapis.com/maps/api/geocode/json'
	params 	= {'sensor': 'false', 'address': location}
	r 	= requests.get(url, params=params)
	results = r.json()['results']
	loc	= results[0]['geometry']['location']
	lat	= loc['lat']
	lon	= loc['lng']

trainbase	= "http://www.transitchicago.com/traintracker/popout.aspx?sid="
trains		= [
	{"line":["red","yellow","purple"], "stop":"Howard", "url":"40900", "lat":42.018769, "long":-87.672535},
	{"line":["red"], "stop":"Jarvis", "url":"41190", "lat":42.015950, "long":-87.669203},
	{"line":["red"], "stop":"Morse", "url":"40100", "lat":42.008298, "long":-87.665963},
        {"line":["red"], "stop":"Loyola", "url":"41300", "lat":42.001154, "long":-87.661049},
        {"line":["red"], "stop":"Granville", "url":"40760", "lat":41.993771, "long":-87.659140},
        {"line":["red"], "stop":"Thorndale", "url":"40880", "lat":41.990262, "long":-87.659054},
	{"line":["red"], "stop":"Addison", "url":"41090", "lat":41.947522, "long":-87.653732}
    ]

distances = {}

for stop in trains:
    a = stop['lat'] - lat
    b = stop['long'] - lon
    c = math.sqrt((a*a) + (b*b))
    distances[stop['url']] = c

for val in sorted(distances.values())[:3]:
    for key, dis in distances.iteritems():
    	if dis == val:
	    url = trainbase+key
    	    req	= requests.get(url)
	    data	= req.text
	    soup	= BeautifulSoup(data, "lxml")
	    train	= []
	    time	= []
	    for i in trains:
		if i['url'] == key:
		    print ' '
		    print i['stop']
		    for j in i['line']:
			print j+' line'
	    for div in soup(attrs={'class' : re.compile(r'^ttar_traindest')}):
	    	train.append(div.text.strip())
	    for div in soup(attrs={'class' : re.compile(r'^ttar_trainpred')}):
	    	time.append(div.text.strip())
	    for i, j in zip(train, time):
	    	info = i+" - "+j
		print info
