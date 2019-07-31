import requests,json,datetime,time

check_id = 'PROC-FF6YT8E1N2-44LJ9L9WQEZ1A4UBIPKR1-J1Z4FX0J-MB'
check_url = 'https://oapi.dingtalk.com/topapi/process/copy'
# get_token_dict= {'appkey':'dingc7d5316ca5582db3',
# 	                 'appsecret':'MLp6OznGapWu-dVOalinRAGl8ttcjoMk15QEZcchupGjCCfCLnqa9BMDUseiu5Yg'}
get_token_dict = {'corpid':'dingc7d5316ca5582db3','corpsecret':"faMFtlHw7QOO2Gmkk6cV85C17g644J8_JlK5eNouy7Er4EwoN9z22yMiWFwnhfRU"}
token_url = 'https://oapi.dingtalk.com/gettoken'
everday_commit_id = 'PROC-FF6YBV6WQ2-AVSFCZ3QTOBGO2AEN2ZV2-57V3XKVI-O' #日常审核ID
def get_token(url,parms):
	#### 获取钉钉授权token的方法，并返回最终授权token
	obj = requests.get(url,params=parms)
	token_info = json.loads(obj.content.decode())
	return token_info.get('access_token')
token_obj = get_token(token_url,get_token_dict)

# #username = {'username':'蒋本乐'}
# url1 = 'https://oapi.dingtalk.com/department/list'
# url4 = 'https://oapi.dingtalk.com/user/simplelist'
# def get_user_id(url,parms):
# 	obj = requests.get(url,params=parms)
# 	user_id = json.loads(obj.content.decode())
# 	print(user_id)
# 	for i in user_id.get('department'):
# 		print(i)
#
#
#
#
# a = "2019-03-08 23:40:00"
# timeArray = time.strptime(a, "%Y-%m-%d %H:%M:%S")
# timeStamp = int(time.mktime(timeArray))
# commit_dict = {'process_code':everday_commit_id,'start_time':timeStamp,'userid_list':'222668330833446511','access_token':token_obj}
# url2 = 'https://oapi.dingtalk.com/topapi/processinstance/listids'
#
# url3 = 'https://oapi.dingtalk.com/user/simplelist'
# def get_everday_commit_info(url,parms):
#
# 	obj = requests.get(url, params=parms)
# 	res = json.loads(obj.content.decode())
# 	print(res)
# #get_user_id(url4,token)
#
# #get_everday_commit_info(url2,commit_dict)

today = (datetime.date.today())
CTCC_special_line= [
	{
		"name": "所属部门",
		"value": "交付中心-数据组"
	},
	{
		"name": "所属项目",
		"value": "P07-06JS出口退税数据分析"
	},
	{
		"name": "项目所属地区",
		"value": "无"
	},
	{
		"name": "申请时间",
		"value": f"{today}"
	},
	{
		"name": "费用类别",
		"value": "网络专线"
	},
	{
		# "ext_value": "{\"isRichText\":false}",
		"name": "申请原因",
		"value": "交付中心数据组建设银行退税项目需要"
	},
	{
		"name": "请款方式",
		"value": "电汇"
	},
	{
		"name": "请款金额（元）",
		"value": "5000"
	},
	{
		# "ext_value": r"{\"isRichText\":false}",
		"name": "对方信息",
		"value": "帐户名称：中国电信股份有限公司大连分公司\n帐 号：100038097390010007\n开户银行：中国邮政储蓄银行大连分行西岗支行\n行 号：403222000182\n收款行SWIFT代码：PSBCCNBJ"
	}
]

CUCC_special_line = [
	{
		"name": "所属部门",
		"value": "交付中心-数据组"
	},
	{
		"name": "所属项目",
		"value": "P07-06JS出口退税数据分析"
	},
	{
		"name": "项目所属地区",
		"value": "无"
	},
	{
		"name": "申请时间",
		"value": f'{today}'
	},
	{
		"name": "费用类别",
		"value": "网络专线"
	},
	{
		# "ext_value": "{\"isRichText\":false}",
		"name": "申请原因",
		"value": "交付中心数据组建设银行退税项目需要"
	},
	{
		"name": "请款方式",
		"value": "电汇"
	},
	{
		"name": "请款金额（元）",
		"value": "6000"
	},
	{
		# "ext_value": "{\"isRichText\":false}",
		"name": "对方信息",
		"value": "业务号：DC00R76507\n开户名:中国联合网络通信有限公司大连市分公司\n账号:100090482700010001\n开户行:中国邮政储蓄银行股份有限公司大连西岗支行\n"
	},

]
def create_task(form_component_values):
	#process_code 是日常费用申请流程的ID号，originator_user_id:  操作人员蒋本乐,dept_id:  部门 总经办ID号
	
	
	url = 'https://oapi.dingtalk.com/topapi/processinstance/create'
	parm_dict = {'process_code':"PROC-FF6YBV6WQ2-AVSFCZ3QTOBGO2AEN2ZV2-57V3XKVI-O",'originator_user_id': "222668330833446511" ,
	             'dept_id': 3542446, 'form_component_values': json.dumps(form_component_values),'access_token':token_obj}
	obj = requests.post(url,params=parm_dict)
	res = json.loads(obj.content.decode())
	return res


