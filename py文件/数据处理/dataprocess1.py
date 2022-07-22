import pandas as pd
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
            if (a + b) > len(data)-1:
                break
        puttog=[data[a][0],data[a][1],data[a][2],data[a][3],data[a][4],','.join(c),data[a][6],data[a][7],data[a][8],data[a][9],data[a][10]]
        d.append(puttog)
        a=a+b
#print(d)
x=pd.DataFrame(d)
x.to_excel(r'C:\Users\WenYuan\Desktop\处理数据_220414-220530 投资事件表.xlsx')













