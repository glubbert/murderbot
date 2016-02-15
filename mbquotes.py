from mbclient import mb
from random import choice
import re,datetime
add_quote="add\s+quote\s+(?P<quote>.+)"
read_quote="(read(?:\s+quote)?|quotes?)(?:\s+(?P<index>[\d]+))?"
random_quote="random(?:\s+quote)?"
search_quote="search\s+(?:quotes?\s+)?(?P<term>.+)"

def random_quote_func(nick,match,target):
	quote=choice(mb.data['quotes'])
	mb.tell(quote['quote'],target,True)
	mb.tell("added by {} on {}".format(quote['added by'],quote['date']),target)
	return

def search_quote_func(nick,match,target):
	results=[]
	term=match.group('term').strip()
	rgx=".*"+re.sub("\s+","\s+",term)
	print(rgx)
	pattern=re.compile(rgx,flags=re.IGNORECASE)
	
	for index,quote in enumerate(mb.data['quotes']):
		if re.search(pattern,quote['quote']):
			results.append(str(index+1))
	if results==[]:
		mb.tell(nick+": nope, none of that",target)
	else:
		mb.tell(nick+", here's what I found ("+str(len(results))+" results): "+", ".join(results),target)
	return

def read_quote_func(nick,match,target):
	index=match.group('index')
	try:
		quote=mb.data['quotes'][int(index)-1]
	except:
		mb.tell(nick+": I got "+str(len(mb.data['quotes']))+" of those here",target)
		return
		
	mb.tell(quote['quote'],target,True)
	mb.tell("added by {} on {}".format(quote['added by'],quote['date']),target)
	return

def add_quote_func(nick,match,target):
	text=match.group('quote')
	date=datetime.date.today().isoformat()
	quote={'quote':text,'added by':nick,'date':date}
	mb.data['quotes'].append(quote)
	mb.save('quotes')
	mb.tell(nick+': added.',target)
	
	return
mb.help["quotes"]="mb add quote <text>, mb read/quote [<index>], mb search <text>, mb random"
print("loaded quotes")
mb.add_command(add_quote,add_quote_func)
mb.add_command(read_quote,read_quote_func)
mb.add_command(search_quote,search_quote_func)
mb.add_command(random_quote,random_quote_func)