from mbclient import mb
import json,urllib
whow="^how.*"
whow_pic="^show\s+me\s+how.*"
def whow_func(nick,match,target):
	headers={'X-Mashape-Key': '6SRh5ZIyhhmshOjLLIEVlfRzZR3Mp1KJgLsjsny2Vq36opmhI6',
			'Accept':'application/json'}
	req=urllib.request.Request('https://hargrimm-wikihow-v1.p.mashape.com/steps?count=3',headers=headers)
	response=urllib.request.urlopen(req).read()
	data=json.loads(response.decode("utf-8"))	
	mb.tell("1.{} 2.{} 3.{}".format(data['1'],data['2'],data['3']),target)
def whow_pic_func(nick,match,target):
	headers={'X-Mashape-Key': '6SRh5ZIyhhmshOjLLIEVlfRzZR3Mp1KJgLsjsny2Vq36opmhI6',
			'Accept':'application/json'}
	req=urllib.request.Request('https://hargrimm-wikihow-v1.p.mashape.com/images?count=1',headers=headers)
	response=urllib.request.urlopen(req).read()
	data=json.loads(response.decode("utf-8"))	
	mb.tell(nick+": "+format(data['1']),target)
mb.add_command(whow,whow_func,priority=3)
mb.add_command(whow_pic,whow_pic_func,priority=3)
mb.help["wikihow"]="mb how <whatever> (random steps from wikihow), mb show me how <whatever> (random picture from wikihow)"
print("loaded wikihow")