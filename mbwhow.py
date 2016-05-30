from mbclient import mb
import json,urllib2
whow="^how.*"

def whow_func(nick,match,target):
	headers={'X-Mashape-Key': '6SRh5ZIyhhmshOjLLIEVlfRzZR3Mp1KJgLsjsny2Vq36opmhI6',
			'Accept':'application/json'}
	req=urllib2.Request('https://hargrimm-wikihow-v1.p.mashape.com/steps?count=3',headers=headers)
	response=urllib2.urlopen(req).read()
	data=json.loads(response.decode("utf-8"))	
	mb.tell(nick+": 1.{} 2.{} 3.{}".format(data['1'],data['2'],data['3']),target)
	
	
	

mb.add_command(whow,whow_func,priority=3)

mb.help["wikihow"]="mb how <whatever> (random steps from wikihow)"


print("loaded wikihow")


