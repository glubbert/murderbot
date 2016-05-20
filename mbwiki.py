# coding: utf-8
from mbclient import mb
from random import choice
import re,json,urllib.parse,urllib.request,traceback
wiki="wiki\s+(?P<r>random\s+)?(?P<what>.+)"
html_tags = re.compile(r'<[^>]+>')

def wiki_func(nick,match,target):
	what = urllib.parse.urlencode({"srsearch":match.group("what")})
	r=match.group('r')
	req = urllib.request.Request('https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext&list=search&'+what)
	try:
		response = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))['query']
		if response['searchinfo']['totalhits']==0:
			mb.tell(nick+": none of that", target)
			return
		else:
			if r:
				result = choice(response['search'])
			else:
				result = response['search'][0]
			mb.tell(result['title'],target)
			mb.tell(re.sub(html_tags,"",result['snippet']),target)

	except:
		mb.tell(nick+": whoops.",target)
		traceback.print_exc()


print("loaded wiki")
mb.help['wiki']="mb wiki <whatever>"
mb.add_command(wiki,wiki_func)