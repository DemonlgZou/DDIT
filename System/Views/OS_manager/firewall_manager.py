import pexpect,paramiko,logging,hashlib,datetime
from io import StringIO



# print(path)
# sys.path.insert(0,path)
####日志模块定义参数####
# log_file = str(datetime.date.today()) + '-info'
# logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#                     datefmt='%a, %d %b %Y %H:%M:%S',
#                     filename='/home/ugw_logs/%s' % log_file,
#                     filemode='a+')

###一旦类方法没找到提示报错#####
def error(self):
    print('对不起不支持功能！')



######支持SSH，SFTP的方法，远程执行命令，上传文件到远端，从远端下载文件到本地######
class Mysftp(object):
    def __init__(self, ip, port, user, pwd=False,key=False):
        self.ip = ip
        self.port = port
        self.user = user
        if pwd :
            self.pwd = pwd
        elif key:
            self.pwd = paramiko.RSAKey(file_obj=StringIO(key))
    def ssh(self, cmd):
        try:
            
            transport = paramiko.Transport(self.ip, self.port)
            transport.connect(username=self.user, password=self.pwd)
            clinet = paramiko.SSHClient()
            clinet.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            clinet._transport = transport
            stdin, stdout, stderr = clinet.exec_command(cmd)
            result = stdout.read()
            error = stderr.read()
            if not error:
                logging.warn('主机%s操作已完成,操作命令是%s' % (self.ip, cmd))
                print(result)
            else:
                logging.error('主机%s操作失败,操作命令是%s' % (self.ip, cmd))
        except TimeoutError as e:

            logging.ERROR('无法连接主机%s' % self.ip)

    def put(self, local_file, remote_file):
        try:

            transport = paramiko.Transport(self.ip, self.port)
            transport.connect(username=self.user, pkey=self.pwd)
            stfp = paramiko.SFTPClient.from_transport(transport)

            stfp.put(local_file, remote_file)
            logging.warn('主机%s操作已完成' % self.ip)
        except TimeoutError as e:
            logging.ERROR('主机%操作错误%s' % (self.ip, e))
        except paramiko.ssh_exception.SSHException as e:
            logging.error('主机%s操作错误%s' % (self.ip, e))

    def get(self, local_file, remote_file):
        try:
            transport = paramiko.Transport(self.ip, self.port)
            transport.connect(username=self.user,password=self.pwd)
            stfp = paramiko.SFTPClient.from_transport(transport)
            stfp.get(remote_file, local_file)
        except TimeoutError as e:
            logging.error('无法连接主机%s' % self.ip)


    def close(self):
        self.close()

a = Mysftp('192.168.254.248',22,'admin','DDit#20020607!')


def ssh_cmd(user, ip, cmd,passwd):
    ssh = pexpect.spawn('ssh %s@%s -p 22' % (user, ip))
    try:
        i = ssh.expect(['password:', 'continue connecting (yes/no)?'], timeout=5)
        if i == 0:
            ssh.sendline(passwd)
        elif i == 1:
            ssh.sendline('yes')
            ssh.expect('password: ')
            ssh.sendline(passwd)
    except pexpect.EOF:
        print("EOF")
    except pexpect.TIMEOUT:
        print("TIMEOUT")
    else:
        ssh.send(cmd)
        r = ssh.read()
        print(r)

    ssh.close()


PROMPT = ['# ', '>>> ', '> ', '\$ ']
def send_command(child, cmd):
    child.sendline(cmd)
    child.expect(PROMPT)
    print(child.before)


def connect(user, host, password):
    ssh_newkey = 'Are you sure you want to continue connecting'
    connStr = 'ssh ' + user + '@' + host
    child = pexpect.spawn(connStr)
    ret = child.expect([pexpect.TIMEOUT, ssh_newkey, '[P|p]assword:'])
    print(ret)
    if ret == 0:
        
        print('[-] Error connecting')
        return
    if ret == 1:
        child.sendline('yes')

    ret = child.expect([pexpect.TIMEOUT, ssh_newkey, '[P|p]assword:'])
    if ret == 0:
        print('[-] Error connecting')

        return

    child.sendline(password)
    child.expect(PROMPT)
    return child


def main():
    host = '192.168.3.189'
    user = 'root'
    password = '1qaz2wsx'
    child = connect(user, host, password)
    send_command(child, 'ls')


if __name__ == '__main__':
    main()
    # user = 'root'
    # host = '192.168.3.189'
    # a = pexpect.spawn('ssh %s@%s'%(user,host))
    # a.expect('Are you sure you want to continue connecting (yes/no)?')
    # a.send('yes +\n')
    # a.expect('[p|P]assword:')
    # a.send('1qaz2wsx +\n')
    # a.expect('\[,\],#')
    #
    # print(a.before)

