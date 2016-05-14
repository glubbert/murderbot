from mbclient import mb
import json,urllib,re
from random import choice
show_me="^show\s+me\s+(?P<query>.*?)(?:\s+#(?P<index>\d+))?$"
lewd = "^lewd\s+(?P<what>[^#]+)(?:#(?P<page>[\d]+))?"


def lewd_func(nick,match,target):
	what = match.group('what')
	query = urllib.parse.urlencode({'s':what})
	page = match.group('page')
	if not page:
		page="1"
	
	try:
		req = urllib.request.Request("http://gif-porn.net/page/"+page+"/?"+query)
		response = urllib.request.urlopen(req).read().decode('utf-8')
	except:
		mb.tell("whoa there hol up something aint right",target)
		return
	pattern = re.compile("<div\s+class=\"entry-content\">.*?(?P<gif>http\S+\.gif).*?</div>", flags=re.DOTALL)
	
	
	gifs = pattern.findall(response)
	mb.tell(nick+": "+choice(gifs),target)
	
	
	

def show_me_func(nick,match,target):
	index = match.group('index')
	if not index:
		index = 0
	else:
		index = int(index)
	headers={'X-Mashape-Key': '6SRh5ZIyhhmshOjLLIEVlfRzZR3Mp1KJgLsjsny2Vq36opmhI6',
			'Accept':'application/json'}
	query=urllib.parse.urlencode({"q":match.group('query')})

	req=urllib.request.Request('https://giphy.p.mashape.com/v1/gifs/search?api_key=dc6zaTOxFJmzC&'+query,headers=headers)
	response=urllib.request.urlopen(req).read()
	results=json.loads(response.decode("utf-8"))["data"]
	
	if results==[]:
		mb.tell(nick+": none of that stuff", target)
		return
	data=results[index]
	gif="https://media.giphy.com/media/{id}/giphy.gif".format(id=data['id'])

	mb.tell(nick+": "+gif,target,True)

		
		
mb.add_command(show_me,show_me_func,priority=3)
mb.add_command(lewd,lewd_func,priority=3)

mb.help["gifs"]="mb show me <whatever> (searches for <whatever> on giphy), mb lewd <whatever> (searches on gif-porn.net)"

print("loaded gifs")



     