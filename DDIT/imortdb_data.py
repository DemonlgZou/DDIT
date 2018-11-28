import xlrd
from db_server import models


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
