from mbclient import mb
import urllib.request
import urllib.parse
import traceback
import re
import json
nsfw="(?:n?sfw\s*(?P<url>.+)?)|((?:is|was)\s+(?:that\s+(?:link|picture|image|pic)|it|that)\s+(?:safe|sfw|nsfw))"
tags="tags?\s+(?P<url>.+)"
emotion="emotions?\s+(?P<url>.+)"
def auth():
	client_id = mb.data["passwords"]["clarifai"]["client_id"]
	client_secret = mb.data["passwords"]["clarifai"]["client_secret"]
	
	data = urllib.parse.urlencode({"client_id": client_id, "client_secret": client_secret, "grant_type":"client_credentials"}).encode("utf-8")
	
	req = urllib.request.Request("https://api.clarifai.com/v1/token",data = data)
	try:
		response = json.loads(urllib.request.urlopen(req).read().decode("utf-8"))
	except:
		traceback.print_exc()
		return ""
	return response["access_token"]



def nsfw_func(nick,match,target):
	link=match.group("url")
	if not link:
		link = mb.data["stuff"]["last_picture"]

	url=urllib.parse.urlencode({"url":link})
	
	
	
	access_token = auth()
	if access_token=="":
		mb.tell(nick+": nope. fucking OAuth",target)
		return
	
	
	
	req = urllib.request.Request("https://api.clarifai.com/v1/tag?model=nsfw-v1.0&{}".format(url));
	req.add_header("Authorization","Bearer "+access_token);
	try:
		response = json.loads(urllib.request.urlopen(req).readall().decode("utf-8"));
	except:
		mb.tell(nick+": something aint right",target)
		traceback.print_exc()
		return
	
	res=response["results"][0]["result"]["tag"];
	mb.tell(nick+": "+res["classes"][0]+": "+"{0:.3f}".format(res["probs"][0])+", "+res["classes"][1]+": "+"{0:.3f}".format(res["probs"][1]),target)



def tags_func(nick,match,target):
	url=urllib.parse.urlencode({"url":match.group("url")})
	access_token = auth()
	if access_token=="":
		mb.tell(nick+": nope. fucking OAuth",target)
		return
	req = urllib.request.Request("https://api.clarifai.com/v1/tag?{}".format(url));
	req.add_header("Authorization","Bearer "+access_token);
	try:
		response = json.loads(urllib.request.urlopen(req).readall().decode("utf-8"));
	except:
		mb.tell(nick+": something aint right",target)
		traceback.print_exc()
		return
	
	res=", ".join(response["results"][0]["result"]["tag"]["classes"])
	mb.tell(nick+": "+res,target)

	return


def emotion_func(nick,match,target):
	url=json.dumps({"url":match.group("url")}).encode("utf-8")
	req = urllib.request.Request("https://api.projectoxford.ai/emotion/v1.0/recognize",data=url);
	req.add_header("Ocp-Apim-Subscription-Key","f40e7a9a0e944f22b1bf91175c0d7e9d");
	req.add_header('Content-Type', 'application/json')
	try:
		response = json.loads(urllib.request.urlopen(req).readall().decode("utf-8"));
	except:
		mb.tell(nick+": something aint right",target)
		traceback.print_exc()
		return
	if response ==[]:
		mb.tell(nick+": no faces on that",target)
		return
		
	faces=[]
	for result in response:
		emotion_list = [{"emotion":emotion,"score":score} for emotion,score in result["scores"].items()]
		emotion_list = sorted(emotion_list, key = lambda k: k["score"])
		
		
		scores = [entry["emotion"] for entry in emotion_list][-2:]
		face = {"emotion": " and ".join(scores), "left": result["faceRectangle"]["left"]}
		faces.append(face)
	
	faces_ordered = sorted(faces, key = lambda k: k["left"])
	emotions= [face["emotion"] for face in faces_ordered]
	
	answer = nick+": "
	if len(response)>1:
		answer+="from left to right: "
	
	
	mb.tell(answer+", ".join(emotions),target)
	
		
		
	
	return
	
mb.add_command(emotion,emotion_func)	
mb.add_command(nsfw,nsfw_func)
mb.add_command(tags,tags_func)
mb.help['recognition']="mb tags <picture url>, mb nsfw <picture url>, mb emotion <picture url>"
print('loaded recognition')