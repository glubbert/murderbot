# coding: utf-8
from mbclient import mb
import urllib,os
import json
import re
languages="(?:what\s+)?languages(?:\s+do|\s+can)?(?:\s+you)?(?:\s+know|\s+speak)?"
can_you_speak="(?:(?:can|do)\s+you\s+(?:know|speak))\s+(?P<lang>[()\w]+)"
translate="translate(?:\s+from\s+(?P<from>[()\w]+))?(?:\s+(?:in)?to\s+(?P<to>[()\w]+))?\s*(?P<text>.+)"
langs= { 
    'ar' : 'Arabic',
    'bg' : 'Bulgarian',
    'ca' : 'Catalan',
    'zh-CHS' : 'Chinese',
    'zh-CHT' : 'Chinese(Traditional)',
    'cs' : 'Czech',
    'da' : 'Danish',
    'nl' : 'Dutch',
    'en' : 'English',
    'et' : 'Estonian',
    'fi' : 'Finnish',
    'fr' : 'French',
    'de' : 'German',
    'el' : 'Greek',
    'ht' : 'Haitian',
    'he' : 'Hebrew',
    'hi' : 'Hindi',
    'hu' : 'Hungarian',
    'id' : 'Indonesian',
    'it' : 'Italian',
    'ja' : 'Japanese',
    'ko' : 'Korean',
    'lv' : 'Latvian',
    'lt' : 'Lithuanian',
    'mww': 'Hmong Daw',
    'no' : 'Norwegian',
    'pl' : 'Polish',
    'pt' : 'Portuguese',
    'ro' : 'Romanian',
    'ru' : 'Russian',
    'sk' : 'Slovak',
    'sl' : 'Slovenian',
    'es' : 'Spanish',
    'sv' : 'Swedish',
    'th' : 'Thai',
    'tr' : 'Turkish',
    'uk' : 'Ukrainian',
    'vi' : 'Vietnamese',
	}
def auth(target):

	client_id=mb.data['passwords']['translate']['client_id']
	client_secret=mb.data['passwords']['translate']['client_secret']

	data = urllib.parse.urlencode({
		'client_id' : client_id,
		'client_secret' :client_secret,
		'grant_type' : 'client_credentials',
		'scope' : 'http://api.microsofttranslator.com'
		})
	uri="https://datamarket.accesscontrol.windows.net/v2/OAuth2-13"
	try:
		response=urllib.request.urlopen(uri,data.encode('utf-8'))
	except urllib.request.HTTPError as e:
		mb.tell("ERROЯ",target)
		print.e.read()
		return None
	rdata=json.loads(response.read().decode('utf-8'))
	if 'access_token' in rdata:
		return rdata['access_token']
	
	return None
	
def can_you_speak_func(nick,match,target):
	lang=match.group('lang')
	for code,language in langs.items():
		if re.search("^"+re.escape(lang)+"$",language,re.IGNORECASE):
			mb.tell(nick+": Yes.",target)
			return
	mb.tell(nick+": No.",target)
	return
	
def languages_func(nick,match,target):
		mb.tell(nick+": "+", ".join(list(langs.values())),target)
		return
		
def translate_func(nick,match,target):
	
	token=auth(target)
	if not token:
		return None
	data={}
	lang_from=match.group('from')
	lang_to=match.group('to')
	if not lang_from:
		lang_from='en'
	if not lang_to:
		lang_to='en'	

	lang_to=lang_to.strip()
	lang_from=lang_from.strip()
	for code,language in langs.items():
		if re.search("^"+re.escape(lang_from)+"$",language,re.IGNORECASE):
			lang_from=code
		if re.search("^"+re.escape(lang_to)+"$",language,re.IGNORECASE):
			lang_to=code
		

	data['from']=lang_from
	data['to']=lang_to
	data['text']=match.group('text')
	
	
	url='http://api.microsofttranslator.com/v2/Http.svc/Translate?'+urllib.parse.urlencode(data)
	print("Translation url request: "+url)
	req=urllib.request.Request(url)
	req.add_header('Authorization','Bearer '+token)
	try:
		response=urllib.request.urlopen(req)
	except urllib.request.HTTPError as e:
		mb.tell("Erroя.",target)
		print(e.read())
		return None
	pattern=re.compile(".*>(?P<tr>.+)<",flags=re.IGNORECASE)
	m=re.match(pattern,response.read().decode('utf-8'))
	mb.tell(nick+": "+m.group('tr'),target)
	return None
mb.add_command(translate,translate_func)
mb.add_command(languages,languages_func)
mb.add_command(can_you_speak,can_you_speak_func)
mb.help['translation']="mb languages, mb do you speak <language>, mb translate from <language> to <language> <text to translate> (languages default to english if not specified)"
print("loaded translation")