# coding: utf-8
from mbclient import mb
from random import choice
import json,urllib,urllib2,traceback
urban = "urban(?:(?P<r>\s+random)|(?P<s>\s+sound))?\s+(?P<what>.+)"


def urban_func(nick,match,target):
	what = urllib.urlencode({"term":match.group("what")})
	s=match.group('s')
	r=match.group('r')
	req = urllib2.Request('https://mashape-community-urban-dictionary.p.mashape.com/define?'+what)
	req.add_header("X-Mashape-Key","6SRh5ZIyhhmshOjLLIEVlfRzZR3Mp1KJgLsjsny2Vq36opmhI6")
	req.add_header("Accept", "text/plain")
	try:
		response = json.loads(urllib2.urlopen(req).read().decode('utf-8'))
		
		if response['result_type'] == "no_results":
			mb.tell(nick+": none of that", target)
			return
		
		if s:
			mb.tell(choice(response['sounds']),target)
		else:
			if r:
				result = choice(response['list'])
			else:
				result = response['list'][0]
			mb.tell(" ".join(result['definition'].splitlines())[:200],target)
			mb.tell("example: "+" ".join(result['example'].splitlines())[:200],target)
		
		
	except:
		mb.tell(nick+": whoops.",target)
		traceback.print_exc()

print("loaded urban")
mb.add_command(urban,urban_func)
mb.help['urban']="mb urban <something>"