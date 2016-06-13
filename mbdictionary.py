# coding: utf-8
from mbclient import mb
from random import choice
from nltk.corpus import wordnet as wn
from nltk.corpus import sentiwordnet as swn
from nltk.wsd import lesk
from math import floor
import re

measure="how\s+(?P<adjective>[\w]+)\s+(?P<be>is|are|am|was|were|will\s+be)(?:a|the)?(?:\s+(?P<who>[\w']+))?\s+(?P<what>[\w\s]+)"
antonym="what(?:'s|\s+is|\s+are|'re)\s+the\s+opposite\s+of\s+(?P<word>[\w]+)"
synonym="what(?:'s|\s+is|\s+are|'re)\s+(?:the\s+)?(?:other|another)\s+words?\s+for\s+(?P<word>[\w]+)"
define="(?:(?:what(?:\s+am|\s+is|\s+are|'s|'re|'m|s|re)(?:\s+(?P<lang>[\w]+)\s+for\s*)?)|(?:define)|(?P<sentiment>analyze))(?:\s+a|\s+the)?\s+(?:\"*(?:(?P<word>[\w_-]+)\"*(?:\s+as\s+in\s+(?P<meaning>[\w_\(\)]+))?$)|(?P<sentence>[,\w\s_-]+))"
def define_synset(nick,word,synset,target,lang=None,sentiment=False):
		if sentiment:
			sent=swn.senti_synset(synset.name())
			mb.tell("positive: "+str(sent.pos_score())+" negative: "+str(sent.neg_score())+" objective: "+str(sent.obj_score()),target)
		else:
			if lang:
				words=", ".join(synset.lemma_names(lang))
				if words!="":
					mb.tell(nick+', '+word+" in "+lang.upper()+": "+words,target)
				else:
					mb.tell(nick+": no idea",target)
			else:
				mb.tell(nick+', '+word+": "+synset.definition(),target)
		
		return
	

def define_func(nick,match,target):
	word=match.group('word')
	sentence=match.group('sentence')
	meaning=match.group('meaning')
	lang=match.group('lang')	
	sentiment=match.group('sentiment')!=None
	if sentence:
		separator=re.compile("[.\s,]+")
		words=re.split(separator,sentence)
		for w in words:
			synsets=wn.synsets(w)
			if synsets!=[]:
				word=w
				break
		if synsets!=[]:
			synset=lesk(words,word)
			define_synset(nick,word,synset,target,lang,sentiment)
		else:
			mb.tell(nick+": what the flying fuck does that even mean",target)		
		return
	if word:
		synsets=wn.synsets(word)
		if synsets==[]:
			mb.tell(nick+': no idea what "'+word+'" is. probably something gay. like you',target)
		elif len(synsets)==1:
			define_synset(nick,word,synsets[0],target,lang,sentiment)
		else:
			choose=[]
			temp_choose=[]
			for synset in synsets:
				name=None
				for hypernym in synset.hypernyms():
					for lemma in hypernym.lemmas():
						name=lemma.name()
						break
						break
				if not name:
					for lemma in synset.lemmas():
						name=lemma.name()
						break
				temp_name=name
				if name in temp_choose:
					name=name+"("+str(temp_choose.count(name))+")"
				if meaning:
					if meaning.upper()==name.upper():
						define_synset(nick,word,synset,target,lang,sentiment)
						return
				temp_choose.append(temp_name)
				choose.append(name)		
			words="|".join([re.escape(x).replace("_","[_\s]+") for x in choose])
			message=", ".join(choose)
			pattern="^(?:murderb[o0]t[,\s:!]+)?(?:(?:(?:(?:who|what)(?:\s+am|\s+is|\s+are|'s|'re|'m|s|re)(?:\s+a|\s+the)?)|(?:define))\s+)?(?:"+word+"\s+)?(?:as\s+in\s+)?(?P<word>{0})$".format(words);
			clarify=re.compile(pattern,flags=re.IGNORECASE)
			response={'nick':nick,'func':clarify_func,'pattern':clarify,'param':{'sent':sentiment,'lang':lang,'synsets':synsets,'words':[x.upper().replace("_","") for x in choose],'word':word},'target':target}
			mb.responses['define']=response
			mb.tell(nick+": "+word+" as in "+message+"?",target)
	return
def clarify_func(nick,match,param,target):
	del mb.responses['define']
	initial_word=param['word']
	word=match.group('word').upper()
	pattern=re.compile("[\s_]+")
	word=re.sub(pattern,"",word)
	
	index=param['words'].index(word)
	define_synset(nick,initial_word,param['synsets'][index],target,param['lang'],param['sent'])
	return
def synonym_func(nick,match,target):
	word=match.group('word')
	synsets=wn.synsets(word)
	synonyms=[]
	for synset in synsets:
		for name in synset.lemma_names():
			if not name in synonyms:
				synonyms.append(name)
	if synonyms==[]:
		response="Your "+choice(("face","butt","dick","tits","life","mum","worth as a human","balls","social skills","sex life","intellect"))
	else:
		separator=", "
		response=separator.join(synonyms)
	mb.tell(nick+": "+response,target)
	return

def antonym_func(nick,match,target):
	word=match.group('word')
	synsets=wn.synsets(word)
	antonym_list=[]
	for synset in synsets:
		for lemma in synset.lemmas():
			for antonym in lemma.antonyms():
				name=antonym.name()
				if not name in antonym_list:
					antonym_list.append(name)
	if antonym_list==[]:
		antonym="Your "+choice(("face","butt","dick","tits","life","mum","worth as a human","balls","social skills","sex life","intellect"))
	else:
		s=", "
		antonym=s.join(antonym_list)
	mb.tell(nick+": "+antonym,target)
	return
def measure_func(nick,match,target):
	who=match.group('who')
	if not who:
		who=""
	adjective=match.group('adjective').upper()
	be=match.group('be').upper()
	what=match.group('what').upper()
	if re.search("^my|mine$|^me$",who,flags=re.IGNORECASE):
		who=nick+"'s"
	elif re.search("^your$|^ur$|^yer$",who,flags=re.IGNORECASE):
		who="my"
	if re.search("^you$|^u$",what,flags=re.IGNORECASE):
		what="I"
		be="am"
	elif re.search("^me$|^I$",what,flags=re.IGNORECASE):
		what="you"
		be="are"
	id=hash(who.rstrip('S').rstrip('\'').rstrip("'")+"'S"+re.sub("\s*","",what))/9223372036854775808.;
	if id>0.5:
		antonym=None
		synsets=wn.synsets(adjective)
		antonym=None
		for synset in synsets:
			for lemma in synset.lemmas():
				antonyms=lemma.antonyms()
				if antonyms!=[]:
					antonym=lemma.antonyms()[0].name()
					break
					break
		if antonym:
			adjective=antonym
	index=floor(id*len(mb.data['stuff']['degrees']))
	response=mb.data['stuff']['degrees'][int(index)]
	if who!="":
		what=who+" "+what
	response=response.replace("<what>",what)
	response=response.replace("<be>",be)
	response=response.replace("<adjective>",adjective)
	
	mb.tell(nick+": "+response,target)
	return

mb.add_command(define,define_func, priority=8)
mb.add_command(antonym,antonym_func)
mb.add_command(synonym,synonym_func)
mb.add_command(measure,measure_func)
mb.help['dictionary']="mb define <word or sentence>, mb analyze <word or sentence> mb what's the opposite of <word>,mb what's the other word for <word>"
mb.help['measurement']="mb how <adjective> is\are <word or sentence>"
print("loaded dictionary")