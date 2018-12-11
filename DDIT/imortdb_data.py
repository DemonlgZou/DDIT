import xlrd,datetime
from db_server import models

def add_contacts():
    #导入供货商相关信息
    data = xlrd.open_workbook('采购联系名单_商户明细-改20170612.xlsx')
    table = data.sheet_by_name('Sheet1')
    nrows = table.nrows
    cols = table.ncols
    t= 0
    for i in range(0,int(nrows)):
        if t not in [0,8,12,13,16,17,19,23,25,27]:
            info =(table.row_values(i))
            print(info)
            name = info[2]
            Address = info[3]
            phone = info[4]
            contacts = info[5]
            Type = info[1]
            bill = info[-1]
            buyer = info[0]
            models.Company_info.objects.create(name=name,Address=Address,phone=phone,contacts=contacts,type=Type,bill=bill,buyer=buyer)
        t+=1



def add_pm_list():
    #导入项目详细信息的脚本
    data = xlrd.open_workbook(r'D:\DDIT\Pmanager\Views\人月数据表.xlsx')
    table = data.sheet_by_index(0)
    nrows = table.nrows
    cols = table.ncols
    t = 0
    for i in range(0, int(nrows)):
            if t >0:
                info = table.row_values(i)
                operator = info[0]
                no = info[1]
                service2in = info[2]
                manager = info[3]
                service2out = info[4]
                father_name = info [5]
                child_name = info[6]
                contract_start = info[7]
                contract_end = info[8]
                pm = info[-1]
                data = {'operator':operator,'pid':no,'service2in':service2in,'service2out':service2out,'father_name':father_name,'child_name':child_name,
                        'manager':manager,'Manage':pm}
                models.PM_list.objects.create(**data)
            t +=1


def add_work_hour():
    ##导入人力工时信息数据
    data = xlrd.open_workbook(r'D:\DDIT\Pmanager\Views\人月数据表.xlsx')
    table = data.sheet_by_name('Sheet1')
    nrows = table.nrows
    cols = table.ncols
    t = 0
    for i in range(0, int(nrows)):
        if t > 0:
            info = table.row_values(i)
            arr1 = float(info[0]) if (info[0]) else 0
            arr2 = float(info[1]) if (info[1]) else 0
            arr3 = float(info[2]) if (info[2]) else 0
            arr4 = float(info[3]) if (info[3]) else 0
            arr5 = float(info[4]) if (info[4]) else 0
            arr6 = float(info[5]) if (info[5]) else 0
            arr7 = float(info[6]) if (info[6]) else 0
            arr8 = float(info[7]) if (info[7]) else 0
            arr9 = float(info[8]) if (info[8]) else 0
            arr10 = float(info[9]) if (info[9]) else 0
            arr11 = float(info[10]) if (info[10]) else 0
            arr12 = float(info[11]) if (info[11]) else 0
            item = info[-1]
            id = models.PM_list.objects.get(pid=item).id
            models.Work_hours.objects.create(arr1=arr1,arr2=arr2,arr3=arr3,arr4=arr4,arr5=arr5,arr6=arr6,arr7=arr7,arr8=arr8,arr9=arr9,arr10=arr10,arr11=arr11,arr12=arr12,item_id=id)
        t +=1
        
        
        

def add_hetong():
    #导入合同相关数据
    data = xlrd.open_workbook(r'C:\Users\demonlg\Desktop\book1.xls')
    table = data.sheet_by_index(1)
    nrows = table.nrows
    cols = table.ncols
    t = 0
    for i in range(0, int(nrows)):
        if t > 0:
            info = table.row_values(i)
            print(info[1:8])
            contract_id = info[1]
            contract_start = info[2]
            contract_end = info[3]
            contract_price = str(info[4])
            contract_work = info[5]
            pid = info[7]
            step = info[10]
            date_time = str(info[11])
            # models.PM_list.objects.filter(pid=pid).update(**{'contract_id':contract_id,
            #                                            'contract_start':contract_start,
            #                                            'contract_end':contract_end,
            #                                            'contract_price':contract_price,
            #                                            'contract_work':contract_work,
            #                                            })
            models.PM_list.objects.filter(pid=pid).update(**{'date_time':date_time,'step':step})
        t +=1
        
        
def add_lichengbei1():
    data = xlrd.open_workbook(r'C:\Users\demonlg\Desktop\book12.xls')
    table = data.sheet_by_index(1)
    nrows = table.nrows
    cols = table.ncols
    t = 0
    for i in range(0, int(nrows)):
        if t >0:
            info = table.row_values(i)
            print(info[7])
            try:
                pid = models.PM_list.objects.get(pid=info[7]).id
                print(pid)
                task1_name = info[12] if info[12] != '' else None
                start_at = info[13]
                end_at =  info[14]
                delay =   info[15]
                plan_no = info[16]
                Evaluation = info[18]
                print(info[12:19])
                #no = info[7]
                models.period.objects.create(**{'name':task1_name,
                                                'start_at':start_at,
                                                'end_at':end_at,
                                                'delay':delay,
                                                'plan_no':plan_no,
                                                'Evaluation':Evaluation
                                                ,'no_id':pid})
            except models.PM_list.DoesNotExist:
                pass
        t +=1
        
        
        
        
def add_lichengbei2():
    data = xlrd.open_workbook(r'C:\Users\demonlg\Desktop\book12.xls')
    table = data.sheet_by_index(1)
    nrows = table.nrows
    cols = table.ncols
    t = 0
    for i in range(0, int(nrows)):
        if t >0:
            info = table.row_values(i)
            print(info[7])
            try:
                pid = models.PM_list.objects.get(pid=info[7]).id
                print(pid)
                task1_name = info[19] if info[19] != '' else None
                start_at = info[20]
                end_at =  info[21]
                delay =   info[22]
                plan_no = info[23]
                Evaluation = info[24]
                print(info[19:25])
                #no = info[7]
                models.period.objects.create(**{'name':task1_name,
                                                'start_at':start_at,
                                                'end_at':end_at,
                                                'delay':delay,
                                                'plan_no':plan_no,
                                                'Evaluation':Evaluation
                                                ,'no_id':pid})
            except models.PM_list.DoesNotExist:
                pass
        t +=1
        
        
        
def write_data():
    #写入资产数据
    data = xlrd.open_workbook(r'D:\DDIT\db_server\1111111.xlsx')
    table = data.sheet_by_index(1)
    nrows = table.nrows
    cols = table.ncols
    t = 0
    for i in range(0, int(nrows)):
        if t > 4:
                info = (table.row_values(i))
               
                name = info[4]
                Type = '台式机'
                CPU = info[5]
                memory = info[7]
                Bios = info[6]
                MAC = info[2]
                SN =info[-1]
                NET =info[13]
                cd =info[12]
                Video =info[10]
                Sound =info[11]
                Disk =info[8]
                user = info[0]
                print(user)
                obj = models.Dictionary.objects.get(id=1)
                arr1 = obj.arr1
                arr2 = obj.arr2
                arr3 = int(obj.arr3)
                new_arr3 = arr3 +1
                models.Dictionary.objects.update(arr3=str(new_arr3).zfill(6))
                No = '%s-%s-%s%s'%(arr1,arr2,str((datetime.datetime.now().year)),str(new_arr3).zfill(6))
                print(No)
               
                print(info[9])
                print(name,Type,CPU,memory,Bios,MAC,SN,NET,cd,Video,Sound,Disk)
                obj = models.host_info.objects.create(name=name,type=Type,CPU=CPU,Memory=memory,Bios=Bios,MAC=MAC,SN=SN,Sound=Sound,Disk=Disk,CDrom=cd,NETWORK=NET,Video=Video)
                models.Reserves.objects.create(name='办公电脑',Type=1,asset_No=No,price=0,company=0,contacts='无',manger_user=info[0],status=1,info_id=obj.id)
                #models.host_info.objects.create(name=info[4],type='显示器',Display=info[9])
        t += 1
#write_data()

def add_port():
    with open(r'C:\Users\demonlg\Desktop\session.log', 'r', encoding='utf-8')as f:
        t = 0
        for line in f:
            # print(line)
            if t > 0:
                a = line.split(' ')
                if 'protocol' in a and 'global' in a and 'interface' in a:
                    rule_name = a[3]
                    rule_type = a[5]
                    interface = a[8]
                    rule_out = a[9]
                    rule_in = a[12]
                    rule_ip = a[11]
                    print(rule_name, rule_in, rule_out, rule_type, rule_ip)
                    models.open_port.objects.create(proposer='管理员',dept='管理员',rule_name=rule_name,
                                                    type=rule_type,host_ip=rule_ip,inside_port=rule_in,
                                                    outside_port=rule_out,on_line=True,interface=interface)
                    
            t += 1
            
