from mbclient import mb
from random import choice
import re


#for later maybe, need to redo how private notices are received for this
#who_will="who(?:\s+and\s+(?P<second>who))?(?P<plural>\s+are|\s+were|'re)?(?P<dowhat>.+)"
eightball=".+"
help="help(?:\s+with)?(?:\s+(?P<cat>\w+))?"

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

	
mb.add_command(help,help_func)
mb.add_command(eightball,eightball_func,priority=999)
mb.help['8ball']=["anything that starts with mb and doesn't fit any other command is treated like an 8ball command"]
print("loaded misc")