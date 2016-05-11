# coding: utf-8
from mbclient import mb
import json,urllib

convert="(?:convert\s+)?(?P<amount>[0-9,e\.\-+\(\)*\/]+)?\s*(?P<what>(?!as\s+)[a-z°'\"]+)\s+(in|to|into)\s+(?P<to>[a-z°'\"]+)\s*$"

def convert_func(nick,match,target):
	amount=match.group('amount')
	if not amount:
		amount="1";
	what=match.group('what')
	to=match.group('to')
	params=urllib.parse.urlencode({"from-type": what,
								"from-value": amount,
								"to-type": to},'utf-8').encode('utf-8')
	headers={"X-Mashape-Key": "6SRh5ZIyhhmshOjLLIEVlfRzZR3Mp1KJgLsjsny2Vq36opmhI6",
			"Content-Type": "application/x-www-form-urlencoded",
			"Accept": "application/json"}
	request = urllib.request.Request("https://community-neutrino-currency-conversion.p.mashape.com/convert",headers=headers,data=params)
	response=urllib.request.urlopen(request).read()
	result=json.loads(response.decode('utf-8'))
	if result['valid']==True:
		mb.tell(nick+": {} {} is {:.4f} {}".format(amount,what,float(result['result']),to),target)
	else:
		mb.tell(nick+": convert these nuts on your chin",target)							
	return 
	
print("loaded conversion")
mb.add_command(convert,convert_func,priority=10)
mb.help["convert"]="mb [convert] <number (defaults to 1)> <units> to/in/into <units>"