# coding: utf-8
from mbclient import mb
import math
import re
calc="calc\s+(?P<expr>[\de*()пpi+-/]+)"

def calc_func(nick,match,target):
	expr=match.group("expr")
	vpi=re.compile("п|pi",flags=re.IGNORECASE)
	ve=re.compile("(?<!\d)e(?!\d)",flags=re.IGNORECASE)
	expr=re.sub(ve,"math.e",expr)
	expr=re.sub(vpi,"math.pi",expr)
	try:
		mb.tell(nick+": "+str(eval(expr)),target)
	except:
		mb.tell(nick+": yeah nah",target)


mb.add_command(calc,calc_func)
mb.help['calculator']="mb calc <expression to calculate>"
print('loaded calculator')