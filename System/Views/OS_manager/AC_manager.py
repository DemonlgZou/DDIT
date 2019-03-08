import pexpect,paramiko,logging,hashlib,datetime,time,telnetlib
from io import StringIO

WIFI_MANAGER_IP = '192.168.96.253'
WIFI_USER = 'admin'
WIFI_PWD = 'merring@her0910'
create_user = 'test'
pwd = '11111'
user_no = '1'


def detele_wifi_user(create_user):
	#删除wifi用户信息
	try:
		a = pexpect.spawn('telnet %s' % WIFI_MANAGER_IP)
		a.expect('login:')
		a.sendline(WIFI_USER)
		a.expect('Password:')
		a.sendline(WIFI_PWD)
		a.expect('<WIFI-AC>')
		a.sendline('sys')
		a.expect('System View')
		a.sendline(f'undo local-user {create_user} class network')
		a.expect('WIFI-AC')
		a.sendline('save main.cfg')
		a.expect('The current configuration will be saved to flash:/main.cfg. Continue?')
		a.sendline('Y')
		a.expect('flash:/main.cfg exists, overwrite?')
		a.sendline('Y')
		a.expect('Configuration is saved to device successfully.')
		a.sendline('save backup.cfg')
		a.expect('The current configuration will be saved to flash:/backup.cfg. Continue?')
		a.expect('flash:/backup.cfg exists, overwrite?')
		a.sendline('Y')
		a.expect('WIFI-AC')
		return True
	except Exception:
		return False




def create_wifi_user(create_user,pwd,user_no):
	# 通过AC创建wifi用户账号的操作命令，create_user是申请人wifi账号，pwd是wifi的登陆密码，user_no是允许最大同时在线的设备数量
	try:
		a = pexpect.spawn('telnet %s' % WIFI_MANAGER_IP)
		a.expect('login:')
		a.sendline(WIFI_USER)
		a.expect('Password:')
		a.sendline(WIFI_PWD)
		a.expect('<WIFI-AC>')
		a.sendline('sys')
		a.expect('System View')
		a.sendline(f'local-user {create_user} class network')
		a.expect('New local user added.')
		a.sendline(f'password simple {pwd}')
		a.expect('WIFI-AC-luser-network-test')
		a.sendline(f'access-limit {user_no}')
		a.expect('WIFI-AC-luser-network-test')
		a.sendline('service-type portal')
		a.expect('WIFI-AC-luser-network-test')
		a.sendline('group ddit')
		a.sendline('quit')
		a.expect('WIFI-AC')
		a.sendline('save main.cfg')
		a.expect('The current configuration will be saved to flash:/main.cfg. Continue?')
		a.sendline('Y')
		a.expect('flash:/main.cfg exists, overwrite?')
		a.sendline('Y')
		a.expect('Configuration is saved to device successfully.')
		a.sendline('save backup.cfg')
		a.expect('The current configuration will be saved to flash:/backup.cfg. Continue?')
		a.expect('flash:/backup.cfg exists, overwrite?')
		a.sendline('Y')
		a.expect('WIFI-AC')
		return True
	except Exception:
		return False




def clean_wifi_user():
	#强制提出用户信息
	try:
		a = pexpect.spawn('telnet %s' % WIFI_MANAGER_IP)
		a.expect('login:')
		a.sendline(WIFI_USER)
		a.expect('Password:')
		a.sendline(WIFI_PWD)
		a.expect('<WIFI-AC>')
		a.sendline('sys')
		a.expect('System View')
		a.sendline(f'portal delete-user username {create_user} ')
		a.expect('WIFI-AC')
		a.sendline('save main.cfg')
		a.expect('The current configuration will be saved to flash:/main.cfg. Continue?')
		a.sendline('Y')
		a.expect('flash:/main.cfg exists, overwrite?')
		a.sendline('Y')
		a.expect('Configuration is saved to device successfully.')
		a.sendline('save backup.cfg')
		a.expect('The current configuration will be saved to flash:/backup.cfg. Continue?')
		a.expect('flash:/backup.cfg exists, overwrite?')
		a.sendline('Y')
		a.expect('WIFI-AC')
		return True
	except Exception:
		return False
#create_wifi_user(create_user,pwd,user_no)  #创建
#detele_wifi_user(create_user)