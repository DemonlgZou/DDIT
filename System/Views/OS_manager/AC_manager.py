import pexpect,paramiko,logging,hashlib,datetime,time,telnetlib,threading
from io import StringIO


WIFI_MANAGER_IP = '192.168.96.253'
WIFI_USER = 'admin'
WIFI_PWD = 'merring@her0910'
#create_user = 'jiangbenle'



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
		a.expect(f'WIFI-AC-luser-network-{create_user}')
		a.sendline(f'access-limit {user_no}')
		a.expect(f'WIFI-AC-luser-network-{create_user}')
		a.sendline('service-type portal')
		a.expect(f'WIFI-AC-luser-network-{create_user}')
		a.sendline('group ddit')
		a.sendline('quit')
		a.expect('WIFI-AC')
		a.sendline('save main.cfg')
		a.expect('The current configuration will be saved to flash:/main.cfg. Continue?')
		#print('baocun')
		a.sendline('Y')
		a.expect('flash:/main.cfg exists, overwrite?')
		#print('queren')
		a.sendline('Y')
		a.expect('Configuration is saved to device successfully.')
		a.sendline('save backup.cfg')
		a.expect('The current configuration will be saved to flash:/backup.cfg. Continue?')
		#print('baocun')
		a.sendline('Y')
		a.expect('flash:/backup.cfg exists, overwrite?')
		#print('queren')
		a.sendline('Y')
		a.expect('WIFI-AC')
		return True
	except Exception:
		return False


def create_wifi_guest(create_user,pwd,start_time,end_time):
	# 通过AC创建wifi访客账号的操作命令，create_user是申请人wifi账号，pwd是wifi的登陆密码，start_time是授权开始时间，end_time是授权结束时间）
	try:
		start_time = start_time.replace('-','/')
		end_time = end_time.replace('-','/')
		a = pexpect.spawn('telnet %s' % WIFI_MANAGER_IP)
		a.expect('login:')
		a.sendline(WIFI_USER)
		a.expect('Password:')
		a.sendline(WIFI_PWD)
		a.expect('<WIFI-AC>')
		a.sendline('sys')
		a.expect('System View')
		a.sendline(f'local-user {create_user} class network guest')
		a.expect('New local user added.')
		a.sendline(f'password simple {pwd}')
		a.expect(f'WIFI-AC-luser-network*')
		a.sendline('group ddit')
		a.expect(f'WIFI-AC-luser-network*')
		a.sendline(f'validity-datetime from {start_time} 00:00:00 to {end_time} 23:00:00')
		a.expect(f'WIFI-AC-luser-network*')
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
		a.sendline('Y')
		a.expect('flash:/backup.cfg exists, overwrite?')
		a.sendline('Y')
		a.expect('WIFI-AC')
		return True
	except Exception:
		return False


def detele_wifi_guest(create_user):
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
		a.sendline(f'undo local-user {create_user} class network guest')
		a.expect('WIFI-AC')
		a.sendline('save main.cfg')
		a.expect('The current configuration will be saved to flash:/main.cfg. Continue?')
		print('baocun')
		a.sendline('Y')
		a.expect('flash:/main.cfg exists, overwrite?')
		print('queren')
		a.sendline('Y')
		a.expect('Configuration is saved to device successfully.')
		a.sendline('save backup.cfg')
		a.expect('The current configuration will be saved to flash:/backup.cfg. Continue?')
		print('back')
		a.sendline('Y')
		a.expect('flash:/backup.cfg exists, overwrite?')
		print('queren')
		a.sendline('Y')
		a.expect('Configuration is saved to device successfully.')
		
		return True
	except Exception:
		return False


def clean_wifi_user(create_user):
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
		#print(create_user)
		a.sendline('save main.cfg')
		a.expect('The current configuration will be saved to flash:/main.cfg. Continue?')
		#print('baocun')
		a.sendline('Y')
		a.expect('flash:/main.cfg exists, overwrite?')
		#print('queren')
		a.sendline('Y')
		a.expect('Configuration is saved to device successfully.')
		a.sendline('save backup.cfg')
		a.expect('The current configuration will be saved to flash:/backup.cfg. Continue?')
		#print('back')
		a.sendline('Y')
		a.expect('flash:/backup.cfg exists, overwrite?')
		#print('queren')
		a.sendline('Y')
		a.expect('Configuration is saved to device successfully.')
		return True
	except Exception:
		return False
	
def change_wifi_pwd(user,pwd):
	a = pexpect.spawn('telnet %s' % WIFI_MANAGER_IP)
	a.expect('login:')
	a.sendline(WIFI_USER)
	a.expect('Password:')
	a.sendline(WIFI_PWD)
	a.expect('<WIFI-AC>')
	a.sendline('sys')
	a.expect('System View')
	a.sendline(f'local-user {user} class network')
	a.expect(f'WIFI-AC-luser-network-{user}')
	#print(111)
	a.sendline(f'password simple {pwd}')
	a.expect(f'WIFI-AC-luser-network-{user}')
	#print(222)
	a.sendline('save main.cfg')
	a.expect('The current configuration will be saved to flash:/main.cfg. Continue?')
	#print('baocun')
	a.sendline('Y')
	a.expect('flash:/main.cfg exists, overwrite?')
	#print('queren')
	a.sendline('Y')
	a.expect('Configuration is saved to device successfully.')
	a.sendline('save backup.cfg')
	a.expect('The current configuration will be saved to flash:/backup.cfg. Continue?')
	#print('back')
	a.sendline('Y')
	a.expect('flash:/backup.cfg exists, overwrite?')
	#print('queren')
	a.sendline('Y')
	a.expect('Configuration is saved to device successfully.')
#create_wifi_guest(create_user,pwd,start_time,end_time)  #创建
#clean_wifi_user(create_user)

#change_wifi_pwd('jiangbenle','123456')
#detele_wifi_guest('jiangbenle')
#create_wifi_user(create_user,'12345678','2')
#detele_wifi_user('jiangbenle')