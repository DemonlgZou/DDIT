import pexpect,paramiko,logging,hashlib,datetime,time,telnetlib,traceback
from io import StringIO
#from db_server import models
import  logging

ddit_collect = logging.getLogger("collect")
ddit_error = logging.getLogger('error')

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
      a.expect(today+'*')
      #print(a.before,a.after)
      a.sendline('quit')
      a.expect('<USG6300>')
      a.sendline('save')
      a.expect('Are you sure to continue?')
      a.sendline('Y')
      a.expect('USG6300')

      return True
  except Exception as e :
      ddit_error.error(e)
      return False


def close_port(ip, user, pwd, rule_name, ):
    # 操作防火墙开放端口的命令
    try:
        #print(rule_name)
        today = datetime.datetime.now().date()
        today = str(today).replace('-', '/')
        # print(today)
        remove_port_cmd = 'undo nat server %s' % (
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
        a.sendline(remove_port_cmd)
        a.expect(today)
        #print(a.before,a.after)
        a.sendline('quit')
        a.expect('<USG6300>')
        a.sendline('save')
        a.expect('Are you sure to continue?')
        a.sendline('Y')
        a.expect('USG6300')
        return True
    except Exception as e:
        ddit_error.error(e)
        return False



def add_up_flow(ip,user,pwd,host_ip,mask):
    try:
        #保障流量
        today = datetime.datetime.now().date()
        today = str(today).replace('-', '/')
        a = pexpect.spawn('telnet %s' % ip)
        a.expect('Username:')
        a.sendline(user)
        a.expect('Password:')
        a.sendline(pwd)
        a.expect('<USG6300>')
        # print(a.before,a.after)
        a.sendline('sys')
        a.expect('Enter system view')
        a.sendline('policy-based-route')
        a.expect('USG6300-policy-pbr')
        a.sendline('rule name jfzx_data_nat1')
        a.expect('USG6300-policy-pbr-rule-jfzx_data_nat1')
        a.sendline(f'source-address {host_ip} mask {mask}')
        a.expect('USG6300-policy-pbr-rule-jfzx_data_nat1')
        a.sendline('quit')
        a.expect(today + '*')
        a.sendline('quit')
        a.expect('USG6300')
        a.sendline('quit')
        a.expect('<USG6300>')
        a.sendline('save')
        a.expect('Are you sure to continue?')
        a.sendline('Y')
        a.expect('USG6300')
        return True
    except Exception as e:
        ddit_error.error(e)
        return False
   


def canlce_keep_up_flow(ip,user,pwd,host_ip,mask):
    try:
        # 取消保障流量
        today = datetime.datetime.now().date()
        today = str(today).replace('-', '/')
        a = pexpect.spawn('telnet %s' % ip)
        a.expect('Username:')
        a.sendline(user)
        a.expect('Password:')
        a.sendline(pwd)
        a.expect('<USG6300>')
        a.sendline('sys')
        a.expect('Enter system view')
        a.sendline('policy-based-route')
        a.expect('USG6300-policy-pbr')
        a.sendline('rule name jfzx_data_nat1')
        a.expect('USG6300-policy-pbr-rule-jfzx_data_nat1')
        a.sendline(f'undo source-address {host_ip} mask {mask}')
        a.expect(today + '*')
        a.sendline('quit')
        a.expect('USG6300-policy-pbr-rule')
        a.sendline('quit')
        a.expect('USG6300')
        a.sendline('quit')
        a.expect('<USG6300>')
        a.sendline('save')
        a.expect('Are you sure to continue?')
        a.sendline('Y')
        a.expect('USG6300')
        return True
    except Exception as e :
        ddit_error.error(e)
        return False

#add_up_flow('192.168.254.248','admin','DDit#20020607!','192.168.0.1','255.255.255.255')
#canlce_keep_up_folw('192.168.254.248','admin','DDit#20020607!','192.168.0.1','255.255.255.255')
