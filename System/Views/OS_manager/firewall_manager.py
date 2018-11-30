import pexpect,paramiko,logging,hashlib,datetime
from io import StringIO

def open_port(ip,user,pwd,cmd):
   #操作防火墙开放端口的命令
  try:
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
      a.sendline(cmd)
      a.expect('2018/11/28')
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


def create_vm():
    pass
   #vm_type1 kvm
