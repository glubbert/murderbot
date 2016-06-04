from mbclient import mb
import urllib, urllib2,json
weather = "weather(?:\s+(?P<F>f|fahrenheit))?(?:\s+(?P<when>tomorrow|(?:in\s+(?:(?P<days>\d+)\s+days))|(?P<week>in\s+a\s+week)|(?P<two_weeks>in\s+two\s+weeks)))?.*\s+(?P<city>.+)"


def weather_func(nick, match,target):
	F = match.group('F')
	if F:
		units = "imperial"
		degrees = "F"
		speed ="m/h"
	else:
		units = "metric"
		degrees = "C"
		speed = "m/s"
		
	when = match.group('when')
	days = match.group('days')
	week = match.group('week')
	two_weeks = match.group('two_weeks')
	if not when:
		function = "weather"
	else:
		function = "daily"
		if tomorrow:
			days = 0
		elif if week:
			days = 6
		elif if week:
			days = 13

		if int(days)>16:
			mb.tell(nick+": what am I nostradamus?? 6 days max")
			return
		
		
		
	city=match.group('city')
	req=urllib2.Request("http://api.openweathermap.org/data/2.5/{}?q={}&appid=dea3debc697fe27920ae5166c6e6594e&units={}&cnt=16".format(function,city,units))
	
	try:
		response=urllib2.urlopen(req)
		result=json.loads(response.read().decode('utf-8'))
	except:
		mb.tell(nick+": Ouch, you broke something",target)
		return
	
	data = {}
	data['degrees'] = degrees
	data['speed'] = speed
 	
	if func == "weather":
		data['lat']=result['coord']['lon']
		data['lon']=result['coord']['lon']
		data['description']=result['weather']['0']['description']
		data['min']=result['main']['temp_min']
		data['max']=result['main']['temp_max']
		data['humidity']=result['main']['humidity']
		data['wind']=result['wind']['speed']
		data['direction']=result['wind']['deg']
		data['clouds']=result['clouds']['all']
		
		
		
	else:
		data['lat']=result['city']['coord']['lon']
		data['lon']=result['city']['coord']['lon']
		data['description']=result['list'][days]['weather']['description']
		data['min']=result['list'][days]['temp']['temp_min']
		data['max']=result['list'][days]['temp']['temp_max']
		data['humidity']=result['list'][days]['humidity']
		data['wind']=result['list'][days]['speed']
		data['direction']=result['list'][days]['deg']
		data['clouds']=result['list'][days]['clouds']
		
		
	answer = "{lat}lat, {lon}lon:{description},{clouds}% cloudy, temp: {min}-{max}{degrees}, humidity: {humidity}%, wind:{wind}{speed}, direction - {direction} degrees".fomat(**data)
	
	mb.tell(nick+": "+answer,target)
	mb.tell(link,target,True)
	return



mb.help["weather"] = "mb weather [f] [tomorrow|in a week|in a month|in N days] <city>"