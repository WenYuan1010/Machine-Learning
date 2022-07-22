# -*- coding: utf-8 -*-
"""
实现从项目名字中提取产品的功能

Created on 2022年5月27日 12点00分
@author  liutaixing
@version 1.0
"""
import jieba
from tqdm import *
from LAC import LAC
import re
import pandas as pd

#导入数据
df=pd.read_excel('C:/Users/WenYuan/Desktop/project.xlsx')

#借助百度的LAC(词性分析)跑出初步数据
lac = LAC()
project_list = []
for text in tqdm(df['project'],position=0):
    fnl_product = ''
    text=re.sub("[（）]","",text)#去掉项目名称中的（）
    for i in range(len(lac.run(text)[0])):
        if lac.run(text)[1][i] in ['n','nz']:
            fnl_product += lac.run(text)[0][i]
            fnl_product = fnl_product+'、'
        else:
            i=i+1
    fnl_product = fnl_product.strip('、')
    project_list.append(fnl_product)
print(project_list)

#将结果存入df中
df['A']=project_list


#下面的功能是去掉结果中类似项目、实验室等非产品的名词
new_list = []
for l in list(df['A']):
    if pd.isna(l):
        l=''
    l=l.split('、')
    for i in reversed(range(len(l))):
        if l[i] in ['项目','工程','生产线','年','加油站','中心','实验室','道路','厂','扩建工程','路面','工艺技术',
                   '车间','码头','产业园','基地','基础设施','生产基地','站','技改','养殖场','线','变电站','农村',
                   '系列','区','矿山','搅拌站','厂房','改建工程','市政','公路','综合楼','园区','城区','有限公司',
                   '加工厂','加气站','养殖基地','小区','工厂','厂区','县城','矿区','乡镇','产业基地','产业链','屠宰场',
                   '殡仪馆','村','拌合站','分公司','农场','养猪场','广告','病区','水电站','卫生院','医院','社区',
                   '报告书','厨房','特色','店','年产量','余热','工序','多功能','迁建工程','出线路','标签','港区','高温',
                   '原址','存栏','公司','体系','平价','动力','疾病','国道','密封条','柔性','通讯','交通','数控','标识',
                   '房','危废库','弯头','路段','库房','食品级','线束','流水线','服务站','沟','现状','水暖','基础','核心',
                   '混凝土搅拌站','砂场','交通设施','污水处理厂','低温','城','总部','专用线','包装生产线','专业','停车场',
                    '水源地','水利','堤防','景观','日','危废暂存库','海洋','合作社','县','商业','泊位','处理场','定点',
                    '院区','技改工程','亚克力','家庭','用地','棚户区','校区','人民医院','渠道','路','内河','高新区','彩色',
                    '活性','环卫','饰面','料','方案','河流','海域','夹具','质量','井井','开发区','医技','类','育肥场',
                    '阶段','年度','生产能力','人防','低压','工作场所','住宅','高频','镇','市场','环境保护','垃圾处理','主',
                    '单元','110kV升压站','基因','项目组','正极','种猪场','发电厂','法人','电压','干法','示范园','储煤场',
                    '消纳场','支流','功率','历史','雨水','枢纽','石场','公共卫生','间隔','全域','航空航天','尾矿库','住院楼',
                    '学校','城市生活','储能','采气厂','设备', '技术','配件','建筑','零部件','材料','环保','产品','设施','智能',
                    '机械','环境','生活','工业','机制','资源','生态','商品','产能','技改项目','高性能','装置','片区','产业',
                    '医疗','电站', '工艺','线路','生物','污水处理站','平台','用品','河道','水厂','表面','能力','核技术','物流',
                    '高速公路','填埋场','新能源','整体','农业','楼','城市','污水管网','库','风电场','仓库','数字','段','区域',
                    '区块','高端','异地','工具','城乡','能源','医药','科技','部分','功能','中转站','采石场','地面','水洗',
                    '门诊','一次性','报告','智慧','油田','土地','轨道交通','轻质','固体','功能性','流域','高强度','总成',
                    '高压','加工场','农光','经济','光学','业务','城镇','结构','病房','物资','标段','化工','分散式','规模',
                    '文化','生态环境','深度','非标','农机','乡村','标牌','国家','场地','企业','加气','预制件','河段','模块',
                    '通道','风力','异形','灌区','地质','小镇','热源','综合体','地区','矿井','高标准','装配式建筑','示范基地']:
            l.remove(l[i])
    l='、'.join(l)
    new_list.append(l)
print(new_list)

'''
下面实现的功能为：原来：'塑料、薄膜、包装材料'  ；cut_for_search('塑料薄膜包装材料')的结果是'塑料薄膜、包装材料'。
 将二者组合后的结果是'塑料薄膜、包装材料' 也就是说我们舍弃了塑料、薄膜 。 对于该项目的样本来说 这样的操作是可以起到优化
 作用的
 
'''
res_product = []
for fnl_product in new_list:
    s=list(set([*jieba.cut_for_search(fnl_product.replace('、',''),HMM=True)]+fnl_product.split('、')))
    s=sorted(s,key=lambda i:len(i))
    count=0
    for i in reversed(range(len(s))):
        i=i-count
        for j in reversed(range(i)):
            if s[i].find(s[j])>=0 or s[j].find(s[i])>=0:
                if len(s[i])>=len(s[j]):s.remove(s[j])
                else:s.remove(s[i])
                i=i-1
                count=count+1
    res = '、'.join(s)
    res_product.append(res)
print(res_product)

#将结果导出
df['产品']=res_product
df.to_excel('C:/Users/WenYuan/Desktop/产品信息.xlsx',index=False)


