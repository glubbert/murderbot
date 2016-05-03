from mbclient import mb
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

time="time"





hi="(?:hi+|he+llo+|he+y|yo+)[\s,!]+(?:mb|murderb(?:0|o)t|mbot)[\s!\.]*"
mbhi="(?:hi+|he+llo+|he+y|yo+)[!\s\.]*"

thank="(?:tha+nks?\s*(?:you)?)[\s,!]+(?:mb|murderb(?:0|o)t|mbot)[\s!\.]*"
mbthank="(?:tha+nks?\s*(?:you)?)[!\s\.]*"


urwelc=["pay me","love u bb","you're welcome","that's it??? for all this hard work??","what would you boobs do without me"]
hello=["bye","shut up","go away","not you again","hi","hello","uh huh","sigh"]





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
	
mb.add_command(hi,hi_func,call=False)	
mb.add_command(thank,thank_func,call=False)	
mb.add_command(mbhi,hi_func)	
mb.add_command(mbthank,thank_func)	

	
	
	
mb.add_command(daddy,daddy_func,priority=0)	
mb.add_command(parent,parent_func)	

mb.add_command(get,get_func)
mb.add_command(save,save_func, level=1)

mb.add_command(help,help_func)
mb.add_command(time,time_func)
mb.add_command(eightball,eightball_func,priority=999)
mb.help['8ball']="anything that starts with mb and doesn't fit any other command is treated like an 8ball command"
mb.help['memos']="mb save <something> as <name> - saves some text under <name>, mb get <name> - retrieves it"
print("loaded misc")