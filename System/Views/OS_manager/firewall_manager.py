import pexpect,paramiko,logging,hashlib,datetime,time,telnetlib
from io import StringIO
from db_server import models


def open_port(ip,user,pwd,rule_name,type,interface,outside,host_ip,inside):
   #操作防火墙开放端口的命令
  try:
      
      today = datetime.datetime.now().date()
      today = str(today).replace('-','/')
      #print(today)
      add_port_cmd = 'nat server %s protocol %s global interface %s %s inside %s  %s no-reverse' % (rule_name,type,interface,outside,host_ip,inside)
      #print(add_port_cmd)
      a = pexpect.spawn('telnet %s'%ip)
      a.expect('Username:')
      a.sendline(user)
      a.expect('Password:')
      a.sendline(pwd)
      a.expect('<USG6300>')
      #print(a.before,a.after)
      a.sendline('sys')
      a.expect('Enter system view')
      #print(a.before,a.after)
      a.sendline(add_port_cmd)
      a.expect(today)
      #print(a.before,a.after)
      a.sendline('quit')
      a.expect('<USG6300>')
      a.sendline('save')
      a.expect('Are you sure to continue?')
      a.sendline('Y')
      a.expect('USG6300')
      
      return True
  except Exception :
      return False


def colse_port(ip, user, pwd, rule_name, ):
    # 操作防火墙开放端口的命令
    try:
        
        today = datetime.datetime.now().date()
        today = str(today).replace('-', '/')
        # print(today)
        add_port_cmd = 'undo nat server %s' % (
        rule_name)
        # print(add_port_cmd)
        a = pexpect.spawn('telnet %s' % ip)
        a.expect('Username:')
        a.sendline(user)
        a.expect('Password:')
        a.sendline(pwd)
        a.expect('<USG6300>')
        # print(a.before,a.after)
        a.sendline('sys')
        a.expect('Enter system view')
        # print(a.before,a.after)
        a.sendline(add_port_cmd)
        a.expect(today)
        # print(a.before,a.after)
        a.sendline('quit')
        a.expect('<USG6300>')
        a.sendline('save')
        a.expect('Are you sure to continue?')
        a.sendline('Y')
        a.expect('USG6300')
        return True
    except Exception:
        return False



def create_vm():
    pass
   #vm_type1 kvm



