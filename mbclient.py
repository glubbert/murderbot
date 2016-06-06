import sys,traceback,os,re,json

try:
	import hexchat
except:
	print("not hexchat it seems")
	
try:
	import irc.client
except:
	print("no irc module")

class mb(irc.client.SimpleIRCClient):
	server = "irc.uworld.se"
	port = 6667
	nickname = "MURDERB0T"
	murdercall=re.compile(r"""
						^
						(?:						#prefix
							murderb[0,o]t   
							|mb
							|mb[0,o]t
						)
						[\s,!?.:]+
						(?P<command>.+)			#then command	
							""",flags=re.IGNORECASE | re.VERBOSE)
	
	
	cstrip=re.compile("\x1f|\x02|\x12|\x0f|\x16|\x1d|\x03(?:\d{1,3}(?:,\d{1,3})?)?", re.UNICODE)
	path=""
	help={}
	admin="glub"
	commands=[]
	
	responses={}
	notices=[]
	connection=None
	data={}
	hexchat=False
	caps=False
	format={
	"BOLD":chr(0x02),"ITALIC":chr(0x1D),"UNDERLINE":chr(0x1F)}
	colors=[
		"WHITE",
		"BLACK",
		"BLUE",
		"GREEN",
		"RED",
		"BROWN",
		"PURPLE",
		"ORANGE",
		"YELLOW",
		"LIME",
		"TEAL",
		"CYAN",
		"LIGHT",
		"PINK",
		"GREY",
		"SILVER"]
	@staticmethod
	def get_data(what):
		return mb.data[what]
	@staticmethod
	def set_data(what,towhat):
		mb.data[what]=towhat
		mb.save(what)
	@staticmethod

	def tell(what,target="",boring=False, action=False):
		if boring:
			quirk=""
		else:
			quirk=mb.data['options']['color']
			quirk+="".join(mb.data['options']['quirk'])
			
			if mb.data['options']['caps']:
				what=what.upper()
		
		what=quirk+what
		
		if not mb.hexchat and action:
			what = "\x01ACTION "+what+"\x01"
	
		
		if mb.hexchat:
			if target=="":
				hexchat.command("timer 0.35 say "+what)
			else:
				print("pming "+target+"...")
				hexchat.command("timer 0.35 msg "+target+" "+what)
		else:
			mb.connection.send_raw("PRIVMSG "+target+" :"+what)
			
	@staticmethod
	def sort_commands():
		mb.commands=sorted(mb.commands, key=lambda k: k['priority'])
	@staticmethod
	def add_command(regex, action, priority=10,level=0,call=True,passive=False):
		pattern=re.compile(regex,flags=re.IGNORECASE)
		command={'pattern':pattern,'action':action,'priority':priority,'level':level,'call':call,'passive':passive}
		mb.commands.append(command)
			
		
		
	@staticmethod
	def execute_command(command,**params):
		try:
			command(**params)
		except SystemExit:
			sys.exit(0)
		except:
			traceback.print_exc()
			print("failed to execute command")
			
	
	@staticmethod
	def respond(message,nick,target):
		for key,response in mb.responses.items():
			if re.search(response['nick'],nick) or response['nick']=="*":
				match=re.match(response['pattern'],message)
				if match:
					if 'param' in response.keys():
						param=response['param']
					else:
						param=None
					params={'nick':nick,'match':match,'target':response['target'],'param':param}
					mb.execute_command(response['func'],**params)
					return True
		return False
		
	@staticmethod
	def execute(message,nick,target):
	
		
	
		if mb.respond(message,nick,target):
			return
		call=re.match(mb.murdercall,message)
		
		if call:
			command=call.group("command")
		else: 
			command=message
		
		
		for entry in mb.commands:
			if entry["call"] and not call:
				continue

			match=re.match(entry['pattern'], command)
			if match:
				params={'nick':nick,'match':match,'target':target}
				func=entry['action']
				if entry['level']==0:
					mb.execute_command(entry['action'],**params)
					print("executing command")
				else:
					notice={'func':func,'params':params,'level':entry['level'],'target':target,}
					mb.notices.append(notice)
					if mb.hexchat:
						hexchat.command("NICKSERV STATUS {}".format(nick))
					else:
						mb.connection.send_raw("NICKSERV STATUS {}".format(nick))
					
					print("sending notice: NICKSERV STATUS {}".format(nick))
				if not entry['passive']:
					return

		
					
	

	
	
	@staticmethod
	def load(what):
		try:
			f=open(os.path.join(mb.path,what+'.json'),'r')
			mb.data[what]=json.loads(f.read())
			f.close()
		except:
			mb.data[what]={}
			print("ERROR: Couldn't load a thing")
			traceback.print_exc()
		
	@staticmethod
	def save(what):
		try:
			f=open(os.path.join(mb.path,what+'.json'),'w')
			f.write(json.dumps(mb.data[what]))
			f.close()
		except:
			print("ERROR: Couldn't save a thing")		
			traceback.print_exc()

	def __init__(self,hexchat=False):
		mb.hexchat=hexchat
		print("init........")
		homedir = os.path.dirname(os.path.realpath('__file__'))
		paths = ["D:/murderbot","/home/batlord/murderbot/murderbot",homedir]
		for path in paths:
			if os.path.isfile(os.path.join(path,"mbclient.py")):
				mb.path = path
				break
		mb.load('uncles')
		mb.load('options')
		mb.load('stuff')
		mb.load('quiz_stats')
		mb.load('quotes')
		mb.load('aliases')
		mb.load('data')
		mb.load('passwords')
		mb.load('interview')
		mb.load('interview_stats')
		mb.load('interview_questions')
		mb.load('yiff')
		mb.load('logs')
		mb.sort_commands()
		if not hexchat:
			irc.client.SimpleIRCClient.__init__(self)
			self.try_connecting()
		
	def on_welcome(self, connection, event):
		print("on_welcome: "+event.arguments[0])
		mb.connection=connection
		connection.send_raw("NICKSERV IDENTIFY JOIrE0UNO");
		for channel in mb.data['options']['to join']:
			connection.join(channel)


	@staticmethod
	def handle_auth(message):
		notice=mb.notices[-1:]
		if notice:
			notice=notice[0]
			pattern=re.compile("STATUS\s+(?P<nick>\S+)\s+(?P<status>\d)",flags=re.IGNORECASE)
			match=re.match(pattern,message).groupdict()
			if match['nick']==mb.admin:
				if int(match['status'])==3:
					mb.execute_command(notice['func'],**notice['params'])
					print('executing...')
					mb.notices.pop()
				else:
					print('expressing doubt')
					mb.tell("are you really "+mb.admin+"? /identify yourself",notice['target'])
			
			elif match['nick'] in mb.data['uncles']:
				if notice['level']>1:
					mb.tell(match['nick']+" You're not my real dad!",notice['target'])
				else:
					if int(match['status'])==3:
						mb.execute_command(notice['func'],**notice['params'])
						print('executing...')
						mb.notices.pop()
					else:
						print('expressing doubt')
						mb.tell("are you really "+match['nick']+"? /identify yourself.",notice['target'])
			else:
				print('dissing the chump')
				mb.tell(match['nick']+": who the fuck are you again",notice['target'])
	

	def on_privnotice(self,connection,event):
		mb.handle_auth(event.arguments[0])

	
	def on_pubnotice(self,connection,event):
		nick=re.sub(mb.cstrip,"",event.source.nick)
		print(nick)
		message=re.sub(mb.cstrip,"",event.arguments[0])
		print(message)
	
	def on_pubmsg(self,connection,event):
		nick=re.sub(mb.cstrip,"",event.source.nick)
		message=re.sub(mb.cstrip,"",event.arguments[0])
		self.execute(message,nick,event.target)
		
	def on_privmsg(self,connection,event):
		nick=re.sub(mb.cstrip,"",event.source.nick)
		message=re.sub(mb.cstrip,"",event.arguments[0])
		try:
			print("(priv)"+nick+": "+message)
		except:
			traceback.print_exc()
		
		mb.execute(message,nick,event.source.nick)

	def try_connecting(self):
		try:
			self.connect(mb.server, mb.port, mb.nickname)
		except irc.client.ServerConnectionError as x:
			print(x)
			sys.exit(1)
		
				
	def on_disconnect(self, connection, event):
		print("disconnected.......")
		self.try_connecting()
