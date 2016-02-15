from mbclient import mb
import sys,traceback
try:
	import mbcommands
except:
	print("failed to import commands :(")
	traceback.print_exc()
try:
	import mbcolor
except:
	print("failed to import colors :(")
	traceback.print_exc()
try:
	import mbtranslation
except:
	print("failed to import translation :(")
	traceback.print_exc()
try:
	import mbdictionary
except:
	print("failed to import dictionary :(")
	traceback.print_exc()
try:
	import mbbing
except:
	print("failed to import bing search :(")
	traceback.print_exc()
try:
	import mbwhow
except:
	print("failed to import wikihow :(")
	traceback.print_exc()
try:
	import mbquiz
except:
	print("failed to import quiz :(")
	traceback.print_exc()
try:
	import mbconvert
except:
	print("failed to import conversion :(")
	traceback.print_exc()
try:
	import mbquotes
except:
	print("failed to import quotes :(")
	traceback.print_exc()
try:
	import mbmisc
except:
	print("failed to import misc :(")
	traceback.print_exc()
	
if __name__=="__main__":
	server = "irc.rizon.sexy"
	port = 6667
	nickname = "murderb0t"
	mbot = mb()
	mb.sort_commands()
	try:
		mbot.connect(server, port, nickname)
	except irc.client.ServerConnectionError as x:
		print(x)
		sys.exit(1)
	mbot.start()
