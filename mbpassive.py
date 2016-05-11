from mbclient import mb
import datetime


picture="(.*\s+)*(?P<link>\S+\.(?:png|jpg|jpeg|gif)\S*)(\s+.*)*"
anything".*"


def picture_func(nick,match,target):
	mb.data["stuff"]["last_picture"]=match.group("link")
	mb.save("stuff");
	
	
	
def deliver_message_func(nick,match,target):
	if "messages" in nick mb.data['logs'][nick]:
		for message in nick mb.data['logs'][nick]['messages']:
			mb.tell(message.nick+" said: "+message.text,nick)
		nick mb.data['logs'][nick]['messages']=[]
	return
	

def  last_message_func(nick,match,target):		
	date = datetime.date.today().isoformat()
	message = match.group(0)
	mb.data['logs'][nick]={'message':message,'date':date}
	mb.save('logs')
	
	
print("loaded passive functions")
mb.add_command(picture,picture_func,call=False, passive= True)	

mb.add_command(anything,last_message_func,call=False, passive=True)	
mb.add_command(anything,deliver_message_func,call=False,passive=True)