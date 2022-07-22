# -*- coding: utf-8 -*-
"""
采集化妆品企业信息

Created on 2022年1月29日 16点00分
@author  zhangjiayang
@version 1.0
"""

import dbutil
import requests
from urllib.parse import urlencode
import json
import random
import time

# 获取请求内容信息
def getPageContent(page, productName = ""):
    # URL地址
    url = 'http://scxk.nmpa.gov.cn:81/xk/itownet/portalAction.do?method=getXkzsList&on=true'

    # 请求参数
    params = {
        "page": page,
        "pageSize": 15,
        "productName": productName,
        "conditionType": 1,
        "applyname":"",
        "applysn":""
    }
    agent_headers = [
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
        "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
        'Opera/9.25 (Windows NT 5.1; U; en)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
        'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
        'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
        "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
        "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0",
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident / 7.0; rv: 11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.30"
    ]

    # 请求头
    headers = {
        "User-Agent": random.choice(agent_headers),
        "Content-Type": "application/x-www-form-urlencoded;utf-8",
        "Origin": "http://scxk.nmpa.gov.cn:81",
        "Referer": "http://scxk.nmpa.gov.cn:81/xk/",
        "X-Requested-With": "XMLHttpRequest",
        "Host": "scxk.nmpa.gov.cn:81"
        #"Upgrade-Insecure-Requests": "1"
    }
    # 这里有个细节，如果params需要json形式的话，需要做处理
    requestUrl = url + "&" + urlencode(params)
    # print(requestUrl)
    try:
        # 关闭忽略SSL连接的告警提示
        requests.packages.urllib3.disable_warnings()
        response = requests.post(requestUrl, None, headers=headers, proxies = [], verify=False)
        # 也可以直接将data字段换成json字段，2.4.3版本之后支持
        # response  = requests.post(url, json = body, headers = headers)

        if response.status_code == 200:
            # 返回信息
            responseText = response.text
            if responseText == "":
                print("返回数据为空")
                return {
                    "errcode": -1,
                    "errmsg": "返回数据为空"
                }
            else:
                responseData = json.loads(responseText)
                return {
                    "errcode": 0,
                    "errmsg": "ok",
                    "data": responseData["list"]
                }
        else:
            # 返回响应头
            print("错误码: %d" % response.status_code)
            return {
                "errcode": -1,
                "errmsg": "发生系统错误,错误码：%d" % response.status_code
            }
    except requests.exceptions.ChunkedEncodingError as err:
        print("发生错误：%s" % err)
        return {
            "errcode": -1,
            "errmsg": "发生系统错误：%s" % err
        }
    except Exception as err:
        print("发生错误：%s" % err)
        return {
            "errcode": -1,
            "errmsg": "发生系统错误：%s" % err
        }

#爬取数据
def crawlWebsiteData(startPage, endPage, productName = ""):
    mysqlSetting_chains = {
        'host': "localhost",
        'port': 3307,
        'user': "root",
        'passwd': "123456",
        'db': "industry_chains",
        'charset': 'utf8'
    }
    connection = dbutil.get_connection(mysqlSetting_chains)
    for page in range(startPage, endPage + 1):
        print("开始采集第%d页数据=============>" % page)
        responseData = getPageContent(page, productName)
        msgCode = responseData["errcode"]
        if msgCode == 0:
            productData = responseData["data"]
            if len(productData) > 0:
                saveProductData(connection, productData)
            else:
                print("返回数据为空")
                break
        else:
            print(responseData["errmsg"])
        print("<=============结束采集第%d页数据" % page)
        randomSleeTime = random.randint(2, 10)
        print("-----睡眠%d秒后重新抓取数据-----" % randomSleeTime)
        time.sleep(randomSleeTime)
    #connection.commit()
    connection.close()

# 保存数据
def saveProductData(connection, productData):
    save_sql = """
        replace into t_cosmetics_companies(id, company_name, credict_code, product_sn, manager_name, expire_date, issue_date) 
         values(%s, %s, %s, %s, %s, %s, %s)
    """
    for product in productData:
        # print(product)
        param = (
            product["ID"],
            product["EPS_NAME"],
            product["BUSINESS_LICENSE_NUMBER"],
            product["PRODUCT_SN"],
            product["QF_MANAGER_NAME"],
            product["XK_DATE"],
            product["XC_DATE"]
        )
        dbutil.execute_sql(connection, save_sql, param, True)

if __name__ == "__main__":
    crawlWebsiteData(1, 50, "")