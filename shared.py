from datetime import datetime
def time_dict(a):
	s=(a-datetime(2016,1,1)).total_seconds()
	hours = s // 3600
	minutes = s%3600 // 60
	seconds = s%60
	when={'hours':hours,'minutes':minutes,'seconds':seconds}
	return when
	

def time_diff(a,b):
	hours = a['hours'] - b['hours']
	minutes = a['minutes'] - b['minutes']
	seconds = a['seconds'] - b['seconds']
	result=""
	if hours>0:
		result+=str(int(hours))+ " hrs "
	if minutes>0:
		result+=str(int(minutes))+ " min "
	if seconds>0:
		result+=str(int(seconds))+ " secs "
	result+="ago"
	return result
		
	