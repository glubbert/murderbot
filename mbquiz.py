from mbclient import mb
from random import choice
import json,urllib,re
from xml.sax.saxutils import unescape
quiz="quiz[\s!?]*$"
quiz_champ="quiz\s+champion[!?\s]*$"
show_quiz_stats="quiz\s+stats(?:\s+for\s+(?P<name>\S+))?[!?\s]*"
aka="aliases(?:\s+for\s+(?P<who>\S+))?"
add_aliases="remember:\s*(?P<name>\S+)\s+is(?P<no>n't|\s+not)?\s+(?P<aliases>\S+)"
purge_aliases="forget\s+(?P<name>\S+)"
points="(?P<do>give|take)\s+(?P<number>\d+)\s+points?\s+(?:from|to)\s+(?P<name>\S+)"
separation=re.compile("\s+and\s+|[,\s]+")

html_tags = re.compile(r'<[^>]+>')

def purge_aliases_func(nick,match,target):
	name=match.group('name')
	if not name in mb.data['aliases']:
		mb.tell(nick+": literally who",target)
	else:
		del mb.data['aliases'][name]
		mb.save('aliases')
		mb.tell(nick+": bam, done",target)

def points_func(nick,match,target):
	do=match.group('do')
	who=None
	name=match.group('name')
	number=int(match.group('number'))
	if name in mb.data['quiz_stats']:
		who=name
	else:
		for player in mb.data['aliases']:
			if who in mb.data['aliases'][player] and player in mb.data['quiz_stats']:
				who=player
	if not who:
		mb.tell(nick+": what points you fuck",target)
		return
	if match.group('do').upper()=='GIVE':
		mb.data["quiz_stats"][who]["answers"]+=number
	else:
		mb.data["quiz_stats"][who]["answers"]-=number
	mb.save("quiz_stats")
	mb.tell(nick+": aight, done",target)
	
def add_aliases_func(nick,match,target):
	
	name=match.group('name')
	no=match.group('no')
	aliases=re.split(separation,match.group('aliases'))
	
	if no:
		if name in mb.data['aliases']:
			mb.data['aliases'][name]=list(set(mb.data['aliases'][name])-set(aliases))
		else:
			mb.tell(nick+": who?...",target)
			return
	else:
		if name in mb.data['aliases']:
			mb.data['aliases'][name]=list(set(mb.data['aliases'][name])| set(aliases))
		else:
			mb.data['aliases'][name]=aliases
	mb.save('aliases')
	mb.tell(nick+": alright done",target)
	
def quiz_champ_func(nick,match,target):
	max=0
	champs=[]
	for name,score in mb.data['quiz_stats'].items():
		if score['answers']==max:
			champs.append(name)
		elif score['answers']>max:
			champs=[name]
			max=score['answers']
	if max==0:
		tell("{}: there are none, you're all losers".format(nick))
		return
	if len(champs)==1:
		plural=""
		be="IS"
	else:
		plural="S"
		be="ARE"
	mb.tell("{}: the current quiz champion{} {} {} with {} answers".format(nick,plural,be,", ".join(champs),str(max)),target)
	return
	
def show_quiz_stats_func(nick,match,target):
	name=match.group('name')
	if not name:
		name=nick
	
	for player in mb.data['aliases']:
		if name in mb.data['aliases'][player]:
			name=player
	
	if not name in mb.data['quiz_stats']:
		mb.tell('that chump never even played',target)
	else:
		stats=mb.data['quiz_stats'][name]
		mb.tell(name+" stats: "+", ".join("{}:{}".format(key,val) for key,val in stats.items()),target)
	return
def quiz_func(nick,match,target):
	if 'quiz' in mb.responses:
		mb.tell("weak! the answer was "+mb.responses['quiz']['param']['answer'],target)
		del mb.responses['quiz']
	req=urllib.request.Request('http://jservice.io/api/random')
	response=urllib.request.urlopen(req).read().decode('utf-8')
	data=choice(json.loads(response))
	answer=re.sub(html_tags,"",data['answer'])
	answer=answer.replace(r"\'","'")	
	answer=unescape(answer)
	mb.tell("Category: {}".format(data['category']['title']),target)
	mb.tell(re.sub(html_tags,"",unescape(data['question']))+" Answer: "+re.sub("[a-zA-Z0-9]","*",answer),target)			
	pattern=re.compile("^(?:murderb[o0]t|mb)?[,\s:!]*"+re.escape(answer)+"\s*$",flags=re.IGNORECASE)
	answer_response={'func':quiz_answer,'pattern':pattern,'nick':".*",'param':{'answer':answer},'target':target}
	mb.responses['quiz']=answer_response
	print(data['question'])
	print(data['answer'])
	return	
def quiz_answer(nick,match,target,param):
	who=None
	if nick in mb.data['quiz_stats']:
		who=nick
	for player in mb.data['aliases']:
		if nick in mb.data['aliases'][player]:
			who=player
			break

	if who:
		mb.data['quiz_stats'][who]['answers']+=1
	else:
		mb.data['quiz_stats'][nick]={'answers':1}
	del mb.responses['quiz']
	mb.tell(nick+": correct! good job nerd.",target)
	mb.save('quiz_stats')
	return
	
def aka_func(nick,match,target):
	who=match.group('who')
	lst=None
	if not who:
		who=nick
	if who in mb.data['aliases']:
		lst=mb.data['aliases'][who]
	else:
		for player in mb.data['aliases']:
			if who in mb.data['aliases'][player]:
				lst=mb.data['aliases'][player]
				who=player
				break
			
	if not lst:
		lst=['big nerd']
	mb.tell("{}, a.k.a {}".format(who,", ".join(lst)),target)
	
	return
mb.help["quiz"]="mb quiz, mb quiz stats [for <name>], mb quiz champion, mb aliases [for <name>]"
mb.add_command(add_aliases,add_aliases_func,level=2)
mb.add_command(purge_aliases,purge_aliases_func,level=2)
mb.add_command(points,points_func,level=2)
mb.add_command(aka,aka_func)
mb.add_command(quiz,quiz_func)
mb.add_command(show_quiz_stats,show_quiz_stats_func)
mb.add_command(quiz_champ,quiz_champ_func)
print("loaded quiz")
