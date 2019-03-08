import requests,json,datetime,time

check_id = 'PROC-FF6YT8E1N2-44LJ9L9WQEZ1A4UBIPKR1-J1Z4FX0J-MB'
check_url = 'https://oapi.dingtalk.com/topapi/process/copy'
get_token_dict= {'appkey':'dingc7d5316ca5582db3',
	                 'appsecret':'MLp6OznGapWu-dVOalinRAGl8ttcjoMk15QEZcchupGjCCfCLnqa9BMDUseiu5Yg'}
token_url = 'https://oapi.dingtalk.com/gettoken'
def get_token(url,parms):
	
	obj = requests.get(url,params=parms)
	token_info = json.loads(obj.content.decode())
	return token_info
token_obj = get_token(token_url,get_token_dict)
print(token_obj)

obj = requests.post(check_url,{'process_code':check_id},headers={'access_token':token_obj.get('access_token')})
print(obj.content)