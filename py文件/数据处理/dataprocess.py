# -*- coding: utf-8 -*-
"""
实现 投资方的合并 和 企业全称与简称的分离

Created on 2022年5月30日 23点00分
@author  liutaixing
@version 1.0
"""

import pandas as pd

###实现投资方的合并

#导入文件
data=pd.read_excel(io=r'C:\Users\WenYuan\Desktop\220414-220530 投资事件表.xlsx')
data=data.values
a = 0
d = []
while a <= len(data)-1:#a溢出则停止
    b = 1
    if (a+b)>len(data)-1: # 此时表示a定位到了最后一个事件ID
        c = []
        c.append(data[a][5])
        puttog = [data[a][0], data[a][1], data[a][2], data[a][3], data[a][4], ','.join(c), data[a][6], data[a][7],data[a][8], data[a][9], data[a][10]]
        d.append(puttog)
    else:
        c = []
        c.append(data[a][5])
        while pd.isna(data[a + b][0]):
            c.append(data[a + b, 5])
            b = b + 1
            if (a + b) > len(data)-1: #溢出则跳出循环
                break
        puttog=[data[a][0],data[a][1],data[a][2],data[a][3],data[a][4],','.join(c),data[a][6],data[a][7],data[a][8],data[a][9],data[a][10]]
        d.append(puttog)
        a=a+b


### 下面将全称与简称分离开
data=d
d=[]
for i in range(len(data)):
    if data[i][2]=='--':
        a = ''
        puttoge=[data[i][0],data[i][1],data[i][2],a,data[i][3],data[i][4],data[i][5],data[i][6],data[i][7],data[i][8],data[i][9],data[i][10]]
        d.append(puttoge)
    elif data[i][2][-1]==')':
        a = data[i][2][data[i][2].rfind('(') + 1:-1]
        puttoge = [data[i][0], data[i][1],data[i][2][0:data[i][2].rfind('(')], a,  data[i][3], data[i][4], data[i][5], data[i][6], data[i][7],data[i][8], data[i][9],data[i][10]]
        d.append(puttoge)
    else:
        a = ''
        puttoge = [data[i][0], data[i][1],  data[i][2],a, data[i][3], data[i][4], data[i][5], data[i][6], data[i][7],data[i][8], data[i][9],data[i][10]]
        d.append(puttoge)
x=pd.DataFrame(d)

#导出文件
x.to_excel(r'C:\Users\WenYuan\Desktop\处理数据_220414-220530 投资事件表.xlsx')












