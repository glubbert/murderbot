import urllib.request
import urllib.parse
from random import choice
import json
from mbclient import mb

what_color="#(?P<hex>[\d,a-f]{6})\s*"
keyword_color="(?:what(?:'s|s|\s+is|\s+are)\s+)?(?:a\s+|the\s+)?colou?rs?\s+(?:for|of)\s+(?P<kw>[\w\s]+)"

def keyword_color_func(nick,match,target):
		keywords=match.group('kw')
		parameters=urllib.parse.urlencode({'keywords':keywords})
		req=urllib.request.Request("http://www.colourlovers.com/api/colors?"+parameters+"&format=json&numResults=20")
		req.add_header('User-Agent', "ColourLovers Browser")
		try:
			response=urllib.request.urlopen(req)
			cdict=choice(json.loads(response.read().decode('utf-8')))
		except IndexError:
			mb.tell(nick+": no idea",target)
			return
		title="'"+cdict['title']+"'"
		hex=cdict['hex']
		link="http://www.colourlovers.com/img/"+hex+"/600/600"
		mb.tell(nick+": "+"#"+hex+", "+title,target)
		mb.tell(link, target)
		return

def what_color_func(nick,match,target):
	color=match.group('hex')
	req=urllib.request.Request("http://www.colourlovers.com/api/color/"+color+"?format=json")
	req.add_header('User-Agent', "ColourLovers Browser")
	try:
		response=urllib.request.urlopen(req)
		cdict=json.loads(response.read().decode('utf-8'))[0]
	except IndexError:
		mb.tell(nick+": did you pull that out of your ass?? shove it back")
		return
	title="'"+cdict['title']+"'"
	link="http://www.colourlovers.com/img/"+color+"/600/600"
	mb.tell(nick+": "+title+" ",target)
	mb.tell(link,target)
	return
mb.add_command(what_color,what_color_func)
mb.add_command(keyword_color,keyword_color_func)
mb.help["colors"]="mb <hex color, e.g. #ff00ff>, mb what's the color of <something>"
print("loaded colors")