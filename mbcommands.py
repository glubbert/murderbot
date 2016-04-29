from mbclient import mb
import re,sys
separation=re.compile("\s+and\s+|[,\s]+")
add_uncle="(?P<names>.+)\s+(?:is|are)(?:now)?(?P<not>\s+not|n't)?\s+your\s+(?:uncles?|aunts?)\s*(?:now|anymore)?$"
type_in="(?P<no>don't\s+|do\s+not\s+)?type\s+(?:in\s+)?(?P<options>.+)"
font_options="font\s+options"
join="join\s+#?(?P<channel>\S+)$"
leave="leave\s+#?(?P<channel>\S+)$"
on_start="(?P<no>(?:don't|do\s+not)\s+)?join\s+#?(?P<channel>\w+)\s+(?:on\s+start(?:\s*up)?|automatically)"
reload="reload\s+(?P<thing>.+)"
shut_down="shut\s+down"
list_uncles="who(?:\s+is|\s+are|'s|'re)\s+your\s+(?:uncles?|aunts?)"

def shut_down_func(nick,match,target):
	mb.tell("bye",target)
	mb.connection.disconnect(message="fuck you all uwu")
	sys.exit(0)
	

def reload_func(nick,match,target):
	mb.load(match.group('thing'))
	mb.tell("Done. Probably.",target)
def font_options_func(nick,match,target):
	lst=list(mb.format.keys())
	clrs=[color.lower() for color in mb.colors]
	lst=[el.lower() for el in lst]
	mb.tell(nick+": format: "+", ".join(lst)+", colors: "+", ".join(clrs),target)
	
def join_func(nick,match,target):
	mb.tell(nick+": ok",target)
	
	mb.connection.join("#"+match.group('channel'))
	
	


def leave_func(nick,match,target):
	mb.tell(nick+": ok",target)
	mb.connection.part("#"+match.group('channel'),message="Bye losers.")
	
	
	

def on_start_func(nick,match,target):
	channel="#"+match.group('channel')
	if match.group('no'):
		mb.data['options']['to join']=list(set(mb.data['options']['to join'])-set([channel]))
	else:
		mb.data['options']['to join'].append(channel)
		mb.data['options']['to join']=list(set(mb.data['options']['to join']))
	mb.save('options')
	mb.tell(nick+": ok",target)
	
def list_uncles_func(nick,match,target):
	if mb.data['uncles']==[]:
		mb.tell("I got none",target)
	else:
		mb.tell(nick+": "+", ".join(mb.data['uncles'])+" are my uncles",target)

def add_uncle_func(nick,match,target):
		names=re.split(separation,match.group('names'))
		if match.group('not'):
			mb.data['uncles']=list(set(mb.data['uncles'])-set(names))
			mb.tell(nick+": well thank fuck", target)
		else:

			mb.data['uncles']=list(set(mb.data['uncles']) | set(names))
			mb.tell(nick+": I mean ew but ok", target)
		mb.save('uncles')

def type_in_func(nick,match,target):
		options=re.split(separation,match.group('options'))
		options=[option.upper() for option in options]
		no=match.group("no")
		if "CAPS" in options:
			if no:
				mb.data['options']['caps']=False
			else:
				mb.data['options']['caps']=True
		if "NORMALLY" in options:
			mb.data['options']['quirk']=[]
			mb.data['options']['caps']=False
			mb.data['options']['color']=""
		else:
			quirks=[mb.format[option] for option in options if option in mb.format]
			if no:
				mb.data['options']['quirk']=list(set(mb.data['options']['quirk'])-set(quirks))	
			else:
				mb.data['options']['quirk'].extend(quirks)
				mb.data['options']['quirk']=list(set(mb.data['options']['quirk']))

		for index,color in enumerate(mb.colors):
			if color in options:
				mb.data['options']['color']=chr(0x03)+str(index)
				break
		mb.save('options')
		mb.tell(nick+": I'll try",target)
		
mb.help['typing']="mb type in <options> (only available to selected few, haha losers), mb font options"
		

mb.add_command(shut_down,shut_down_func,level=2)			
mb.add_command(list_uncles,list_uncles_func)			
mb.add_command(reload,reload_func,level=2)		
mb.add_command(add_uncle,add_uncle_func,level=2)
mb.add_command(type_in,type_in_func,level=1)
mb.add_command(font_options,font_options_func,level=1)
mb.add_command(join,join_func,level=2)
mb.add_command(leave,leave_func,level=2)
mb.add_command(on_start,on_start_func,level=2)
print("loaded commands")