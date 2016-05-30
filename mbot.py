import sys,traceback,irc,logging,imp,os
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
	#"mbconvert",
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

if __name__=="__main__":
	
	#logging.basicConfig(filename="murder.log", level=logging.DEBUG)
	mbot = mb()
	print("{} commands".format(len(mb.commands)))
	mbot.start()
