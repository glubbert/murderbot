from mbclient import mb
import json,urllib
from random import choice
show_me="^show\s+me\s+(?P<query>.+)"


def show_me_func(nick,match,target):
	headers={'X-Mashape-Key': '6SRh5ZIyhhmshOjLLIEVlfRzZR3Mp1KJgLsjsny2Vq36opmhI6',
			'Accept':'application/json'}
	query=urllib.parse.urlencode({"q":match.group('query')})

	req=urllib.request.Request('https://giphy.p.mashape.com/v1/gifs/search?api_key=dc6zaTOxFJmzC&'+query,headers=headers)
	response=urllib.request.urlopen(req).read()
	results=json.loads(response.decode("utf-8"))["data"]
	
	if results==[]:
		mb.tell(nick+": none of that stuff", target)
		return
	data=choice(results)
	gif="https://media.giphy.com/media/{id}/giphy.gif".format(id=data['id'])

	mb.tell(nick+": "+gif,target,True)

		
		
mb.add_command(show_me,show_me_func,priority=3)

mb.help["gifs"]="mb show me <whatever> (searches for <whatever> on giphy)"

print("loaded gifs")



     