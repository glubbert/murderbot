from datetime import datetime
def time_dict(a):
	s=(a-datetime(1970,1,1)).total_seconds()
	days = s//86400
	hours = s%86400 // 3600
	minutes = s%3600 //60
	seconds = s%60
	when={'days':days,'hours':hours,'minutes':minutes,'seconds':seconds}
	return when
	

def time_diff(a,b):
	days = a['days'] - b['days']
	hours = a['hours'] - b['hours']
	minutes = a['minutes'] - b['minutes']
	seconds = a['seconds'] - b['seconds']
	result=""
	if days>0:
		result+=str(int(days))+ " days "
	if hours>0:
		result+=str(int(hours))+ " hrs "
	if minutes>0:
		result+=str(int(minutes))+ " min "
	if seconds>0:
		result+=str(int(seconds))+ " sec "
	result+="ago"
	return result
		
	