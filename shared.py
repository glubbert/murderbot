from datetime import datetime
def time_dict(a):
	s=(a-datetime(2016,1,1)).total_seconds()

	return s
	

def time_diff(a,b):
	s = a - b
	hours = s // 3600
	minutes = s%3600 // 60
	seconds = s%60
	result=""
	if hours>0:
		result+=str(int(hours))+ " hrs "
	if minutes>0:
		result+=str(int(minutes))+ " min "
	if seconds>0:
		result+=str(int(seconds))+ " secs "
	result+="ago"
	return result
		
	