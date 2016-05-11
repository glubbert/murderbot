from mbclient import mb
from datetime import datetime
import shared

picture="(.*\s+)*(?P<link>\S+\.(?:png|jpg|jpeg|gif)\S*)(\s+.*)*"
anything=".*"


def picture_func(nick,match,target):
	mb.data["stuff"]["last_picture"]=match.group("link")
	mb.save("stuff");
	
	
	
def deliver_message_func(nick,match,target):
	if nick not in mb.data['logs']:
		return

	if "messages" in mb.data['logs'][nick]:
		for message in mb.data['logs'][nick]['messages']:
			date = datetime.now()
			now=shared.time_dict(date)
			when = message['date']
			time = shared.time_diff(now,when)
			
			
			mb.tell(message['nick']+" said "+time+": "+message['text'],nick)
			
		
		mb.data['logs'][nick]['messages']=[]
		mb.save('logs')
	return
	

def  last_message_func(nick,match,target):		
	date = datetime.now()
	when=shared.time_dict(date)
	
	message = match.group(0)
	print(nick+" said "+message)
	if not nick in mb.data['logs']:
		mb.data['logs'][nick]={}
	mb.data['logs'][nick]['message'] = message
	mb.data['logs'][nick]['date'] = when
	mb.save('logs')
	
	
print("loaded passive functions")
mb.add_command(picture,picture_func,call=False, passive= True,priority=5)	

mb.add_command(anything,last_message_func,call=False, passive=True,priority=5)	
mb.add_command(anything,deliver_message_func,call=False,passive=True,priority=5)