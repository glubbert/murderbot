from mbclient import mb
from random import shuffle,choice
interview="interview\s*(?P<role>detective|suspect)?$"
reset="reset\s+interview"
shoot="(?P<shoot>shoot|bam|bang|replicant)|(?P<dismiss>dismisse?d?|(?:ok[\s,!]+)?you\s+can\s+go|human)"

interview_stats="interview\s+stats(?:\s+for\s+(?P<nick>\S+))?"
interview_init="interview\s+init(?:ialize)?"
next="next(?:\s+question)?"
interview_champion="interview champion"


def interview_champion_func(nick,match,target):
	champs=[]
	record=0
	for name,user in mb.data['interview_stats'].items():
		d_w=user['as detective']['wins']
		r_w=user['as replicant']['wins']
		d_l=user['as detective']['losses']
		r_l=user['as replicant']['losses']
		score=d_w+r_w-r_l-d_l
		if score>record:
			record=score
			champs=[name]
		elif score==record:
			champs.append(name)
	
	if record==0:
		mb.tell(nick+": no champion you all suck",target)
	else:
		mb.tell(nick+": "+", ".join(champs),target)
	
	

def interview_stats_func(nick,match,target):
	who=match.group('nick')	
	if not who:
		who=nick
	for player in mb.data['aliases']:
		if who in mb.data['aliases'][player]:
			who=player
			break
	if who in mb.data['interview_stats']:
		stats=mb.data['interview_stats'][who]
		mb.tell(who+": detective: w-{wins}, l-{losses}".format(**stats['as detective'])+"; replicant: w-{wins}, l-{losses}".format(**stats['as replicant']),target)
	else:
		mb.tell(who+" never played interview",target)
	


def interview_func(nick,match,target):
	mb.load("interview_questions")
	who=nick
	role=match.group("role")
	
	
	
	
	for player in mb.data['aliases']:
		if nick in mb.data['aliases'][player]:
			who=player
			break	
			
	if role:
		if role in mb.data['interview'].keys():
			name = mb.data['interview'][role]	
			mb.tell(nick+": "+name+" called dibs on being a "+role+". get rekt nerd",target)
			return;
		else:
			mb.data['interview'][role]=who	
			
	if not who in mb.data['interview_stats']:
		mb.data['interview_stats'][who]={"as detective":{"wins":0,"losses":0},"as replicant":{"wins":0,"losses":0}}
		mb.save('interview_stats')
		
	if len(mb.data['interview']['players'])==2:	
		mb.tell("wait until the current game ends you poopsquirrel",target)
		return
	else:		
		mb.data['interview']['players'].append(nick)
		mb.data['interview'][nick]=who
		if len(mb.data['interview']['players'])==1:
			mb.tell("Game started, waiting for another player to join.",target)
		else:	
			if "detective" in mb.data['interview']:
				mb.data['interview']['suspect']=mb.data['interview']['players'][1]
			elif "suspect" in mb.data['interview']:
				mb.data['interview']['detective']=mb.data['interview']['players'][1]
		
			else:
				shuffle(mb.data['interview']['players'])
				mb.data['interview']['suspect']=mb.data['interview']['players'][0]
				mb.data['interview']['detective']=mb.data['interview']['players'][1]
		
			fate=choice(['human','replicant'])
			if fate=='human':
				answer="SPEAK TRULY"
			else:
				answer="LIE"
			mb.data['interview']['fate'] = fate
			suspect = mb.data['interview']['suspect']
			detective = mb.data['interview']['detective']

			question=choice(mb.data["interview_questions"])
			mb.data['interview']['questions']=[question]
			
			mb.tell(detective+" is the detective, "+suspect+" is the suspect",target)
			
			
			mb.tell("You're a "+fate+" bruh, that means you are REQUIRED TO "+answer+" answerin' "+detective+"'s questions.",suspect)
			
			mb.tell("You're the detective. Ask this question miss marple, you can paraphrase it:", detective)
			
			
			

			mb.tell(question,detective)
			
			interview_responses(target)
	
	mb.save('interview')
	


def interview_init_func(nick,match,target):
	interview_responses(target)

def interview_responses(target):
	if not "suspect" in mb.data['interview'] or not "detective" in mb.data["interview"]:
		mb.tell("there's no game going",target)
		return
	suspect = mb.data['interview']['suspect']
	detective = mb.data['interview']['detective']
	
	shoot_response={'func':shoot_func,'pattern':shoot,'nick':suspect+'|'+detective,'target':target}
	next_response={'func':next_func,'pattern':next,'nick':detective,'target':target}
	
	mb.responses['interview_shoot']=shoot_response
	print(mb.responses['interview_shoot']);
	mb.responses['interview_next']=next_response
	mb.tell("ok done",target)
	
	
def shoot_func(nick,match,target,param=None):
	
	
	
	suspect=mb.data['interview']['suspect']
	fate=mb.data['interview']['fate']
	detective=mb.data['interview']['detective']
	
	suspect_realname=mb.data['interview'][suspect]
	dick_realname=mb.data['interview'][detective]
	
	
	if match.group('shoot'):
		if nick==suspect:
			if fate=='human':
				mb.tell(suspect+ ': what the fuck is wrong with you, you\'re human, you\'re not even supposed to shoot at all.',target)
				mb.data['interview_stats'][suspect_realname]['as replicant']['losses']+=1
			else:
				mb.tell(suspect+': you killed the detective, no one wins. fucking robots',target)
		
		else:
			if fate=='human':
				mb.tell(detective+': good job fucko you just KILLED a human BEING',target)
				mb.data['interview_stats'][dick_realname]['as detective']['losses']+=1
			else:
				mb.tell(detective+ ': nice shooting bruh one less robot scum',target)
				mb.data['interview_stats'][dick_realname]['as detective']['wins']+=1
				mb.data['interview_stats'][suspect_realname]['as replicant']['losses']+=1
	else:
		if nick==suspect:
			return
		if fate=='human':
			mb.tell(detective+': good jerb',target)
			mb.data['interview_stats'][dick_realname]['as detective']['wins']+=1
			mb.data['interview_stats'][suspect_realname]['as replicant']['losses']+=1
		else:
			mb.tell(detective+ ': haha loser, that was a robot. get REKT',target)
			mb.data['interview_stats'][dick_realname]['as detective']['losses']+=1;
			mb.data['interview_stats'][suspect_realname]['as replicant']['wins']+=1;
		
	mb.data['interview']={'players':[]}
	mb.save('interview')
	mb.save('interview_stats')
	del mb.responses['interview_shoot']
	del mb.responses['interview_next']


def next_func(nick,match,target,param=None):
	if len(mb.data['interview']['questions'])>2:
		mb.tell(nick+": you only get three questions pal, now make up your mind",target)
		return
	detective=mb.data['interview']['detective']
	while True:
		question=choice(mb.data["interview_questions"])
		if question not in mb.data['interview']['questions']:
			break
	mb.data['interview']['questions'].append(question)
	mb.save('interview')
	mb.tell("Here's another one:", detective)
	mb.tell(question, detective)
	

	
def reset_func(nick,match,target):
	mb.tell(nick+": fun cancelled, gotcha",target)
	mb.data['interview']={'players':[]}
	mb.save('interview')
	

mb.help["interview"]="'mb interview' to start\join the game, once you're playing: 'shoot' or 'bam' or 'bang' to shoot the opponent, 'dismiss' or 'you can go' to dismiss, 'next' or 'next question' to get another question"

mb.add_command(interview_champion,interview_champion_func,level=1)
mb.add_command(reset,reset_func,level=1)
mb.add_command(interview_init,interview_init_func)
mb.add_command(interview,interview_func)
mb.add_command(interview_stats,interview_stats_func)
print("loaded interview")