# coding: utf-8
from mbclient import mb
import json,urllib,urllib2,os
bing="bing\s+(?P<query>.+)"
def bing_func(nick,match,target):
	query=urllib.urlencode({"Query":"'"+match.group('query')+"'"})
	try:
		key=mb.data['passwords']['bing']['key']
		req=urllib2.Request("https://api.datamarket.azure.com/Bing/SearchWeb/v1/Web?"+query+"&$top=1&$format=json&Market=%27en-US%27&Adult=%27Off%27")
		req.add_header("Authorization","Basic "+key)
		response=urllib2.urlopen(req).read()
		data=json.loads(response.decode("utf-8"))['d']['results'][0]
		mb.tell(data['Description'],target)
		mb.tell(data['Url'],target,True)	
	except urllib2.HTTPError as er:
		print(er)
		mb.tell("ERROЯ",target)
mb.add_command(bing,bing_func)
print("loaded bing search")
mb.help['bing']="mb bing <text>"