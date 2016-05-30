__module_name__ = "MURDERBOT"
__module_version__ = "6.66"
__module_description__ = "FUCK YOU"
import hexchat,re,os,traceback,sys
import imp

homedir = os.path.dirname(os.path.realpath('__file__'))
path="no path :("




paths = ["D:/murderbot","/home/batlord/murderbot/murderbot",homedir]
for p in paths:
	if os.path.isfile(os.path.join(p,"mbclient.py")):
		path = p
		break

print("the path is: "+path)	

sys.path.append(path)
from mbclient import mb

		
def load(modname):

	handle, pathname, descrip = imp.find_module(modname, [path])
	try:
		return imp.load_module(modname, handle, pathname, descrip)
	except:
		print("failed to import "+modname+" :(")
		traceback.print_exc()
	
modnames=[
	"mbcolor",
	"mbcommands",
	"mbtranslation",
	"mbbing",
	"mbwhow",
	"mbquiz",
	"mbconvert",
	"mbquotes",
	"mbmisc",
	"mbcalc",
	#"mbupdates",
	"mbgifs",
	"mbinterview",
	"mbrecognition",
	"mbpassive",
	"mbwiki",
	"mburban",
	"mbdictionary",
	]
for module in modnames:
	load(module)

			
	
	
cstrip=re.compile("\x1f|\x02|\x12|\x0f|\x16|\x1d|\x03(?:\d{1,3}(?:,\d{1,3})?)?", re.UNICODE)
	
def pmhook(word,word_eol,userdata):	
		nick=re.sub(cstrip,"",word[0])
		message=re.sub(cstrip,"",word[1])
		mb.execute(message,nick,nick)
		return None	
	
	
def cmhook(word,word_eol,userdata):	
		nick=re.sub(cstrip,"",word[0])
		message=re.sub(cstrip,"",word[1])
		mb.execute(message,nick,"")
		return None	
		
def hook_auth(word,word_eol,userdata):	
		nick=re.sub(cstrip,"",word[0])
		message=re.sub(cstrip,"",word[1])
		if nick.upper()=="NICKSERV":
			mb.handle_auth(message)
		return None	


mbot = mb(True)



print(str(len(mb.commands)))
hexchat.hook_print('Notice',hook_auth)
hexchat.hook_print('Private Message to Dialog',pmhook)
hexchat.hook_print('Private Message',pmhook)
hexchat.hook_print('Channel Message',cmhook)
hexchat.hook_print('Channel Msg Hilight',cmhook)		
	
	


