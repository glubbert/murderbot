from mbclient import mb

picture="(.*\s+)*(?P<link>\S+\.(?:png|jpg|jpeg|gif)\S*)(\s+.*)*"

def picture_func(nick,match,target):
	mb.data["stuff"]["last_picture"]=match.group("link")
	mb.save("stuff");
	

	

	
	
print("loaded passive functions")
mb.add_command(picture,picture_func,call=False)	


