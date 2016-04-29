from mbclient import mb
import math
import re
nsfw="nsfw\s+(?P<url>.+)"
tags="tags\s+(?P<url>.+)"

def nsfw_func(nick,match,target):
	expr=match.group("expr")
	vpi=re.compile("п|pi",flags=re.IGNORECASE)
	ve=re.compile("(?<!\d)e(?!\d)",flags=re.IGNORECASE)
	expr=re.sub(ve,"math.e",expr)
	expr=re.sub(vpi,"math.pi",expr)
	try:
		mb.tell(nick+": "+str(eval(expr)),target)
	except:
		mb.tell(nick+": yeah nah",target)


def tags_func(nick,match,target):
	expr=match.group("expr")
	vpi=re.compile("п|pi",flags=re.IGNORECASE)
	ve=re.compile("(?<!\d)e(?!\d)",flags=re.IGNORECASE)
	expr=re.sub(ve,"math.e",expr)
	expr=re.sub(vpi,"math.pi",expr)
	try:
		mb.tell(nick+": "+str(eval(expr)),target)
	except:
		mb.tell(nick+": yeah nah",target)		
		
		
mb.add_command(nsfw,nsfw_func)
mb.add_command(tags,tags_func)
mb.help['recognition']="mb tags <picture url>, mb nsfw <picture url>"
print('loaded calculator')