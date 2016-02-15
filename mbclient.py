import irc.client,sys,traceback,os,re,json


class mb(irc.client.SimpleIRCClient):
	murdercall=re.compile("^(?:murderb[0,o]t|mb|mb[0,o]t)[\s,!?.:]+(?P<command>.+)",flags=re.IGNORECASE)
	path=""
	help={}
	admin="glub"
	commands=[]
	responses={}
	notices=[]
	connection=None
	data={}
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
	def tell(what,target,boring=False):
		if boring:
			quirk=""
		else:
			quirk="".join(mb.data['options']['quirk'])
			quirk+=mb.data['options']['color']
			if mb.data['options']['caps']:
				what=what.upper()
		
		mb.connection.privmsg(target,quirk+what)
	@staticmethod
	def sort_commands():
		mb.commands=sorted(mb.commands, key=lambda k: k['priority'])
	@staticmethod
	def add_command(regex, action, priority=1,level=0):
		pattern=re.compile(regex,flags=re.IGNORECASE)
		command={'pattern':pattern,'action':action,'priority':priority,'level':level}
		mb.commands.append(command)
		
		
		
	@staticmethod
	def execute_command(command,**params):
		try:
			command(**params)
		except SystemExit:
			sys.exit(0)
		except:
			traceback.print_exc()
			
	
	@staticmethod
	def respond(message,nick,target):
		for key,response in mb.responses.items():
			if response['nick']==nick or response['nick']=="*":
				match=re.match(response['pattern'],message)
				if match:
					if 'param' in response.keys():
						param=response['param']
					else:
						param=None
					params={'nick':nick,'match':match,'target':response['target'],'param':param}
					print(params)
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
			return
		for entry in mb.commands:
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
					mb.connection.send_raw("NICKSERV STATUS {}".format(nick))
					print("sending notice: NICKSERV STATUS {}".format(nick))
				return
					
	

	
	
	@staticmethod
	def load(what):
		try:
			f=open(os.path.join(mb.path,what+'.txt'),'r')
			mb.data[what]=json.loads(f.read())
			f.close()
		except:
			mb.data[what]={}
			print("ERROR: Couldn't load a thing")
			traceback.print_exc()
		
	@staticmethod
	def save(what):
		try:
			f=open(os.path.join(mb.path,what+'.txt'),'w')
			f.write(json.dumps(mb.data[what]))
			f.close()
		except:
			print("ERROR: Couldn't save a thing")		
			traceback.print_exc()

	def __init__(self):
		irc.client.SimpleIRCClient.__init__(self)
		mb.path=os.path.dirname(os.path.realpath('__file__'))+"\\"
		mb.load('uncles')
		mb.load('options')
		mb.load('stuff')
		mb.load('quiz_stats')
		mb.load('quotes')
		mb.load('aliases')
		
	def on_welcome(self, connection, event):
		mb.connection=connection
		for channel in mb.data['options']['to join']:
			connection.join(channel)


	

	def on_privnotice(self,connection,event):
		notice=mb.notices[-1:]
		if notice:
			notice=notice[0]
			pattern=re.compile("STATUS\s+(?P<nick>\S+)\s+(?P<status>\d)",flags=re.IGNORECASE)
			match=re.match(pattern,event.arguments[0]).groupdict()
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
					mb.tell(match['nick']+"You're not my real dad!")
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

		

	
	
	def on_pubmsg(self,connection,event):
		nick=event.source.nick
		message=event.arguments[0]	
		self.execute(message,nick,event.target)
		
	def on_privmsg(self,connection,event):
		nick=event.source.nick
		message=event.arguments[0]	
		mb.execute(message,nick,event.target)

				
	def on_disconnect(self, connection, event):
		sys.exit(0)
