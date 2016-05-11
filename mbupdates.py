# coding: utf-8
from mbclient import mb
import urllib,traceback
import re
prequel="prequel"

def prequel_func(nick,match,target):
	try:
		resp=urllib.request.urlopen("http://www.prequeladventure.com/feed").read().decode("utf-8")
		date=re.search("<pubDate>(.*)</pubDate>",resp,re.I).group(1)
		mb.tell(nick+", last update: "+date,target)
	except:
		mb.tell(nick+": ERROЯ",target)
		traceback.print_exc()
		
mb.help["updates"]="mb prequel"		
print("loaded updates")
mb.add_command(prequel,prequel_func)