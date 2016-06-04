from mbclient import mb
import shared
from random import choice
from datetime import datetime
import re


#for later maybe, need to redo how private notices are received for this
#who_will="who(?:\s+and\s+(?P<second>who))?(?P<plural>\s+are|\s+were|'re)?(?P<dowhat>.+)"
eightball=".+"
help="help(?:\s+with)?(?:\s+(?P<cat>\w+))?"
daddy="who'?s?\s+is\s+(?:ur|your)\s+daddy"
parent="who'?s?\s+\is\s+(?:ur|your)\s+(?:father|mother|dad|parent)"
save="save\s+(?P<thing>.+)\s+as\s+(?P<name>.+)"
get="(?:get|fetch|gimme|give)(?:\sme)?\s+(?P<name>.+)|(?:what\s+have\s+you\s+got)"
yiff="yiff\s+(?P<who>.+)"
coin = "choose\s+(?P<what>.+)$"
seen = "(?:have\s+you\s+)?seen\s+(?P<who>\S+)"
send_message="tell\s+(?P<who>\S+)\s+(?P<what>.+)"
time="time"





hi="(?:hi+|he+llo+|he+y|yo+)[\s,!]+(?:mb|murderb(?:0|o)t|mbot)[\s!\.]*"
mbhi="(?:hi+|he+llo+|he+y|yo+)[!\s\.]*"

thank="(?:tha+nks?\s*(?:you)?)[\s,!]+(?:mb|murderb(?:0|o)t|mbot)[\s!\.]*"
mbthank="(?:tha+nks?\s*(?:you)?)[!\s\.]*"


urwelc=["pay me","love u bb","you're welcome","that's it??? for all this hard work??","what would you boobs do without me"]
hello=["bye","shut up","go away","not you again","hi","hello","uh huh","sigh"]


def coin_func(nick,match,target):
	what = match.group('what')
	p=re.compile("\s*(?:and|or|\.|,)+\s*")
	options = p.split(what)
	
	mb.tell(nick+ ": "+choice(options),target)


def yiff_pick(match):
	string = match.group(1)
	quick = re.search("\|",string)
	if quick:
		options=string.split("|")
	else:
		options = mb.data['yiff'][string]
	res = choice(options)
	return res
	

def yiff_func(nick,match,target):
	who=match.group("who")
	if who == "me":
		who = nick
	elif who in ["yourself","urself"]:
		who = mb.nickname
	mb.data['yiff']['caller']=[nick];
	mb.data['yiff']['target']=[who];
	too_much=20
	pattern = re.compile("{([|\w_]+)}")
	yiff = choice(mb.data['yiff']['yiff'])
	while re.search("{",yiff) and too_much>0:
		too_much -= 1	
		yiff=re.sub(pattern,yiff_pick,yiff)
	mb.tell(yiff,target,action=True)
	



def hi_func(nick,match,target):
	mb.tell(nick+": "+choice(hello),target)


def thank_func(nick,match,target):
	mb.tell(nick+": "+choice(urwelc),target)	









def get_func(nick,match,target):
	name=match.group('name')
	if name:
		name=name.lower()
	else:
		name=".*"
	if name in mb.data['data']:
		mb.tell(nick+": "+mb.data['data'][name],target,True)
	else:
		results=[]
		for title, thing in mb.data['data'].items():
			if re.search(name,title+thing, flags=re.IGNORECASE):
				results.append(title)
		if results==[]:
			mb.tell(nick+": dunno anything like that",target)
		else:
			mb.tell(nick+": did you mean "+", ".join(results)+"? you shit? you dumbass?",target)
			

def save_func(nick,match,target):
	name=match.group('name').lower()
	thing=match.group('thing')
	mb.data['data'][name]=thing
	mb.tell(nick+": aight",target)
	mb.save('data')


def help_func(nick,match,target,param=None):
	category=match.group('cat')
	if category in mb.help:
		mb.tell(nick+": "+mb.help[category],target)
	else:
		mb.tell(nick+ ": help with "+", ".join(list(mb.help.keys())),target)
		pattern=re.compile("^(?P<cat>"+"|".join(list(mb.help.keys()))+")$",flags=re.IGNORECASE)
		response={'pattern':pattern,'nick':nick,'target':target,'func':help_func}
		mb.responses['help']=response
	
def eightball_func(nick,match,target):
	mb.tell(nick+": "+choice(mb.data['stuff']['premonition']),target)

def time_func(nick,match,target):
	mb.tell(nick+": "+str(datetime.now().time()),target)
	
def parent_func(nick,match,target):	
	mb.tell("Glub is and it fills me with existential dread and urge to vomit",target)
	
def daddy_func(nick,match,target):
	mb.tell("ew what the fuck is wrong with you",target)

	
	

	
	

def seen_func(nick,match,target):
	who = match.group('who')
	
	
	if who in mb.data['logs']:
		date = datetime.now()
		when = mb.data['logs'][who]['date']
		now=shared.time_dict(date)
		
		time=shared.time_diff(now,when)
		mb.tell(nick+": "+who+" was here "+time+", saying '"+mb.data['logs'][who]['message']+"'",target)
	else:
	
		mb.tell(nick+": never heard of that douche",target)

def send_message_func(nick,match,target):
	who = match.group('who')
	date = datetime.now()
	when=shared.time_dict(date)
	
	message = match.group('what')
	if not who in mb.data['logs']:
		mb.data['logs'][who]={}

	if not 'messages' in mb.data['logs'][who]:	
		mb.data['logs'][who]['messages']=[]
		
	mb.data['logs'][who]['messages'].append({'text':message, 'nick': nick,'date':when})
	

	
	mb.tell(nick+": jeez FINE I'll tell em",target)
	mb.save('logs')
	
	
mb.add_command(send_message,send_message_func)
mb.add_command(seen,seen_func)		
mb.add_command(hi,hi_func,call=False)	
mb.add_command(thank,thank_func,call=False)	
mb.add_command(mbhi,hi_func)
mb.add_command(coin,coin_func)	
mb.add_command(mbthank,thank_func)	
#mb.add_command(daddy,daddy_func,priority=0)	
#mb.add_command(parent,parent_func)	
mb.add_command(yiff,yiff_func)	
mb.add_command(get,get_func)
mb.add_command(save,save_func, level=1)
mb.add_command(help,help_func)
mb.add_command(time,time_func)
mb.add_command(eightball,eightball_func,priority=999)
mb.help['choice'] = "mb choose <list of things separated by , 'or' or 'and'>"
mb.help['seen'] = "mb seen <who>"
mb.help['tell'] = "mb tell <who> <what>"


mb.help['8ball']="anything that starts with mb and doesn't fit any other command is treated like an 8ball command"
mb.help['memos']="mb yiff <someone>, mb save <something> as <name> - saves some text under <name>, mb get <name> - retrieves it"
print("loaded misc")