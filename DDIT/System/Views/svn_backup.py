import os ,argparse,datetime,time
#
# abs_path = os.path.abspath(__file__)
# base_name = os.path.basename(abs_path)
# file_name = os.path.splitext(base_name)[0]
#
# pasrse = argparse.ArgumentParser(prog='SVN_BACK', usage='''本程序用于龙图信息技术公司SVN备份，主要提供增量备份和全量备份功能，涉及到的参数共有8种:
# soucre_dir,desc_file,rversion具体参数使用请输入%s -h查看具体使用命令。
# 1、全量备份单独目录
# 2、增量备份单独目录;
# 3、全量备份所有目录;
# 4,增量备份单独目录。
# ''' % file_name, epilog='''操作实例：
# 1'全量备份单独目录
#
# 2'增量备份单独目录
#
# 3'全量备份所有目录
#
# 4'增量备份单独目录
#
#
# ''' % (file_name, file_name, file_name, file_name))
# pasrse.add_argument('--full','-f',help='备份类型',dest='mode')
# pasrse.add_argument()


import os, datetime,shutil,logging




ip = '192.168.0.20'
source_dir = 'F:\Repositories'  # 要备份文件所在的绝对路径
dest_dir = 'F:\\'  # 要保存文件所在的绝对路径
backup_time = str(datetime.datetime.today().strftime('%Y%m%d%H%M%S'))#备份时间
tmp_dir = 'F:\svn_tmp' #备份文件临时生成的目录
log_file = 'SVN_back.log' #备份操作日志


###定义日志类型和格式
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='%s' % os.path.join(os.path.abspath(dest_dir),log_file),
                    filemode='a+')


def back_svn(source_dir,dest_dir,ip,tmp_dir):
	try:
		os.chdir(source_dir) #切换到要备份的文档库目录下
		if os.path.exists(dest_dir) is False:   #判断备份文件夹是否存在 不存在创建文件夹
			os.makedirs(dest_dir)
		if os.path.exists(tmp_dir) is False:    #判断临时文件夹是否存在 不存在创建文件夹
			os.makedirs(tmp_dir)
		for i in os.listdir(source_dir):     #遍历要备份的SVN版本目录
			source_file = os.path.abspath(i)
			# 判断SVN版本库下面的文件类型
			if os.path.isdir(source_file):    # 是文件夹进行备份
				dest_file = os.path.join(dest_dir, i)
				res = os.system('svnadmin.exe dump ' + source_file + ' > ' + dest_file)
				if res:
					logging.info('SVN版本库%s备份成功'%source_file)
					# version = os.system('svnlook.exe youngest %s') % source_file
					# with open(os.path.join(os.path.abspath(tmp_dir),'svn_version'), 'a', encoding='utf-8') as f:
					# 	f.writelines('%s:%s') % (source_file, str(version))
					# 	logging.info('SVN版本库%s版本号记录成功' % source_file)
					# 	f.flush()
			elif os.path.isfile(source_file):#是文件直接拷贝到临时备份文件夹
				shutil.copy2(source_file,tmp_dir)
				logging.info('SVN版本库%s最新版本号写入成功'%source_file)
		svn_data = os.path.join(os.path.abspath(dest_dir),'%s-SVN-%s'%(ip,backup_time))
		#打包临时备份文件夹内文件到备份文件夹中
		shutil.make_archive(svn_data,'zip',tmp_dir)
		logging.info('%s打包成功'%svn_data)
		shutil.rmtree(os.path.abspath(tmp_dir))
		#删除临时备份文件夹
		logging.info('%s临时文件夹删除成功'%tmp_dir)
	except Exception as e:
		logging.error('操作失败，错误参数：%s'%e)






if __name__ == '__main__':
	
	back_svn(source_dir,dest_dir,ip,tmp_dir)


