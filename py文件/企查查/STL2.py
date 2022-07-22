# -*- coding: utf-8 -*-
"""
实现 企业简称to企业全称 的批量采集 包括 法定代表人 注册资本 电话等

Created on 2022年4月17日 14点00分
@author  liutaixing
@version 1.0
"""
import random
import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import csv
import time
from tqdm import *
import win32api,win32con

time_start=time.time()
#准备用户代理库
USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
    "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
    "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
    "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
    "UCWEB7.0.2.37/28/999",
    "NOKIA5700/ UCWEB7.0.2.37/28/999",
    "Openwave/ UCWEB7.0.2.37/28/999",
    "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999",
    # iPhone 6：
    "Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25"
]

#导入企业简称
inputname=input('请输入导入文件名称：')
df_companys = pd.read_excel(r'C:\Users\WenYuan\Desktop\{}.xlsx'.format(inputname),sheet_name='Sheet1')
companys = df_companys['公司简称'].tolist()

#打开储存企业全称的文件，准备后续写入
outputname=input("请输入输出文件名称：")

#得到cookie信息
def get_cookie(keyword):
    url = 'https://www.qcc.com/web/search?key={}'.format(keyword)
    response = requests.get(url, headers={'User-Agent':random.choice(USER_AGENTS)}, allow_redirects=False)
    response.encoding = 'utf8'
    result = re.findall(r'div>您的请求ID是: <strong>\n(.*?)</strong></div>',  response.text)
    return result[0]


try:
    # 爬取企业全称并存入csv文件
    a = []
    for company in tqdm(companys):
        headers = {
            'user-agent': random.choice(USER_AGENTS),
            'cookie':'qcc_did=07894e4f-cda0-4e8b-a176-cc1fb53bfbf7; UM_distinctid=17f8811b31ecb6-0f6211d9c81289-56171d51-144000-17f8811b31fc64; _uab_collina=165000968522032972050308; acw_tc=7cc8712616532773404304975e1599900ca16f34c3469be92283cabba8; QCCSESSID=8d9d35b94431cbd3e822406744; CNZZDATA1254842228=1295480780-1647246194-https%253A%252F%252Fwww.baidu.com%252F%7C1653275096'
            # 'cookie': 'acw_tc={}'.format(get_cookie(company))  # 使用get_cookie函数
        }
        url = 'https://www.qcc.com/web/search?key={}'.format(company)
        response = requests.get(url, headers=headers)
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, features="html.parser")
        if len(soup.find_all('a', {'class': 'title copy-value'})) == 0:
            ##提醒OK消息框
            win32api.MessageBox(0, "需要去企查查网站验证!!!", "提醒", win32con.MB_OK)
            url = 'https://www.qcc.com/web/search?key={}'.format(company)
            response = requests.get(url, headers=headers)
            response.encoding = response.apparent_encoding
            soup = BeautifulSoup(response.text, features="html.parser")
            if len(soup.find_all('a', {'class': 'title copy-value'})) == 0:
                ##提醒OK消息框
                win32api.MessageBox(0, "需要去企查查网站验证!!!", "提醒", win32con.MB_OK)
                url = 'https://www.qcc.com/web/search?key={}'.format(company)
                response = requests.get(url, headers=headers)
                response.encoding = response.apparent_encoding
                soup = BeautifulSoup(response.text, features="html.parser")
                if len(soup.find_all('a', {'class': 'title copy-value'})) == 0:
                    a.append([company, '', '', '', '', ''])
                    print([company, '', '', '', '', ''])
                elif len(list(soup.find_all('a', {'class': 'title copy-value'})[0].next_siblings)) == 1:
                    company_list = soup.find_all('a', {'class': 'title copy-value'})[0].get_text().strip()
                    legal_representative = soup.find_all('div', {'class': 'rline over-rline'})[0].find('span', {
                        'class': 'val'}).get_text().strip()
                    registered_capital = soup.find_all('div', {'class': 'rline over-rline'})[0].find_all('span', {
                        'class': 'val'})[1].get_text().strip()
                    phone = soup.find_all('div', {'class': 'rline over-rline'})[1].find('span', {
                        'class': 'val'}).get_text().strip()# find只会找第一个。
                    a.append([company, company_list, '', legal_representative, registered_capital, phone])
                    print([company, company_list, '', legal_representative, registered_capital, phone])
                else:
                    company_list = soup.find_all('a', {'class': 'title copy-value'})[0].get_text().strip()
                    management_forms = soup.find_all('a', {'class': 'title copy-value'})[
                        0].next_sibling.next_sibling.get_text().strip()
                    # if management_forms in ['存续','在业']:
                    legal_representative = soup.find_all('div', {'class': 'rline over-rline'})[0].find('span', {
                        'class': 'val'}).get_text().strip()
                    registered_capital = soup.find_all('div', {'class': 'rline over-rline'})[0].find_all('span', {
                        'class': 'val'})[1].get_text().strip()
                    phone = soup.find_all('div', {'class': 'rline over-rline'})[1].find('span', {
                        'class': 'val'}).get_text().strip()
                    a.append([company, company_list, management_forms, legal_representative, registered_capital, phone])
                    print([company, company_list, management_forms, legal_representative, registered_capital, phone])
            elif len(list(soup.find_all('a', {'class': 'title copy-value'})[0].next_siblings)) == 1:
                company_list = soup.find_all('a', {'class': 'title copy-value'})[0].get_text().strip()
                legal_representative = soup.find_all('div', {'class': 'rline over-rline'})[0].find('span', {
                    'class': 'val'}).get_text().strip()
                registered_capital = soup.find_all('div', {'class': 'rline over-rline'})[0].find_all('span', {
                    'class': 'val'})[1].get_text().strip()
                phone = soup.find_all('div', {'class': 'rline over-rline'})[1].find('span', {
                    'class': 'val'}).get_text().strip()
                a.append([company, company_list, '', legal_representative, registered_capital, phone])
                print([company, company_list, '', legal_representative, registered_capital, phone])
            else:
                company_list = soup.find_all('a', {'class': 'title copy-value'})[0].get_text().strip()
                management_forms = soup.find_all('a', {'class': 'title copy-value'})[
                    0].next_sibling.next_sibling.get_text().strip()
                # if management_forms in ['存续','在业']:
                legal_representative = soup.find_all('div', {'class': 'rline over-rline'})[0].find('span', {
                    'class': 'val'}).get_text().strip()
                registered_capital = soup.find_all('div', {'class': 'rline over-rline'})[0].find_all('span', {
                    'class': 'val'})[1].get_text().strip()
                phone = soup.find_all('div', {'class': 'rline over-rline'})[1].find('span', {
                    'class': 'val'}).get_text().strip()
                a.append([company, company_list, management_forms, legal_representative, registered_capital, phone])
                print([company, company_list, management_forms, legal_representative, registered_capital, phone])
        elif len(list(soup.find_all('a', {'class': 'title copy-value'})[0].next_siblings)) == 1:
            company_list = soup.find_all('a', {'class': 'title copy-value'})[0].get_text().strip()
            legal_representative = soup.find_all('div', {'class': 'rline over-rline'})[0].find('span', {
                'class': 'val'}).get_text().strip()
            registered_capital = soup.find_all('div', {'class': 'rline over-rline'})[0].find_all('span', {
                'class': 'val'})[1].get_text().strip()
            phone = soup.find_all('div', {'class': 'rline over-rline'})[1].find('span', {
                'class': 'val'}).get_text().strip()
            a.append([company, company_list, '', legal_representative, registered_capital, phone])
            print([company, company_list, '', legal_representative, registered_capital, phone])
        else:
            company_list = soup.find_all('a', {'class': 'title copy-value'})[0].get_text().strip()
            management_forms = soup.find_all('a', {'class': 'title copy-value'})[
                0].next_sibling.next_sibling.get_text().strip()
            # if management_forms in ['存续','在业']:
            legal_representative = soup.find_all('div', {'class': 'rline over-rline'})[0].find('span', {
                'class': 'val'}).get_text().strip()
            registered_capital = soup.find_all('div', {'class': 'rline over-rline'})[0].find_all('span', {
                'class': 'val'})[1].get_text().strip()
            phone = soup.find_all('div', {'class': 'rline over-rline'})[1].find('span', {
                'class': 'val'}).get_text().strip()
            a.append([company, company_list, management_forms, legal_representative, registered_capital, phone])
            print([company, company_list, management_forms, legal_representative, registered_capital, phone])

except:
    pd.DataFrame(a).to_excel(r'C:\Users\WenYuan\Desktop\{}.xlsx'.format(outputname), index=False,
                             header=['公司简称', '公司全称', '经营状态','法定代表人','注册资本','电话'])
    print('共耗时{}s'.format(time.time() - time_start))
    ##提醒OK消息框
    win32api.MessageBox(0, "企查查爬完了！！！", "提醒", win32con.MB_OK)

else:
    pd.DataFrame(a).to_excel(r'C:\Users\WenYuan\Desktop\{}.xlsx'.format(outputname), index=False,
                             header=['公司简称', '公司全称', '经营状态','法定代表人','注册资本','电话'])
    print('共耗时{}s'.format(time.time() - time_start))
    ##提醒OK消息框
    win32api.MessageBox(0, "企查查爬完了！！！", "提醒", win32con.MB_OK)


