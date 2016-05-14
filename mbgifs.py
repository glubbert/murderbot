from mbclient import mb
import json,urllib,re,traceback
from random import choice,shuffle
show_me="^show\s+me\s+(?P<query>.*?)(?:\s+#(?P<index>\d+))?$"
lewd = "^lewd\s+(?P<what>.+)"



	


def lewd_func(nick,match,target):
	what = match.group('what')
	query = urllib.parse.urlencode({'tag':what})
	
	tumbles = ['deliciousnights','thoughtsandthoughtsoflove','sweet-loving-sex','schnoez','sexornothing','c-opulation',]
	shuffle(tumbles)
	posts = []
	

	result = None
	
	
	for tumble in tumbles:
		try:
			req = urllib.request.Request("https://api.tumblr.com/v2/blog/"+tumble+".tumblr.com/posts/photo?api_key=fuiKNFp9vQFvjLNvx4sUwti4Yb5yGutBN4Xh10LXZhhRKjWlV4&"+query)
			response = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
		except:
			mb.tell("whoa there hol up something aint right",target)
			traceback.print_exc()
			return
		posts = response['response']['posts']
		shuffle(posts)
		
		if posts == []:
			continue
		else:
			for post in posts:
				photo = choice(post['photos'])['original_size']['url']
				if re.search(".gif$",photo):
					mb.tell(nick+": "+photo,target)
					return
		
	mb.tell(nick+": none of that here, what is wrong with you",target)	
		
		
	
	
	
	
	
	
	
	

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



     