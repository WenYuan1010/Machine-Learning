import pandas as pd
data=pd.read_excel(io=r'C:\Users\WenYuan\Desktop\PE、VC库_20190101至20220414.xlsx')
data=data.values
print(data)
d=[]
for i in range(len(data)):
    if pd.isna(data[i][2]):
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
x.to_excel(r'C:\Users\WenYuan\Desktop\处理数据_PE、VC库_20190101至20220414.xlsx')



