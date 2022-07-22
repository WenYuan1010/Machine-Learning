import random
import time
import datetime
import pymysql
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import requests


class Drug(object):

    def __init__(self):
        # 声明一个谷歌驱动器，并设置不加载图片，间接加快访问速度
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # 如何实现让selenium规避被检测的风险
        #self.options.add_argument('headless')  # 设置option

        self.options.add_argument("--disable-blink-features=AutomationControlled")

        self.options.add_argument("--incognito")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument(
            'user-agent="Mozilla/5.0 (Macintosh; U; Mac OS X Mach-O; en-US; rv:2.0a) Gecko/20040614 Firefox/3.0.0 "')
        self.options.add_experimental_option('prefs', {'profile.managed_default_content_settings.images': 2})
        self.options.add_experimental_option('useAutomationExtension', False)
        self.browser = webdriver.Chrome(chrome_options=self.options, port=6070)
        self.browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => fasle
                })
            """
        })

        # 窗口最大化
        self.browser.maximize_window()
        # 隐式等待  wait = browser.implicitly_wait(10)
        # 显示等待
        self.wait = WebDriverWait(self.browser, 10)


    def page_reset(self, url):

        self.browser.get(url)
        self.browser.refresh()
        # self.browser.set_window_size(1920, 1080)
        # 判断网页中是否存在关闭
        element_existance = True
        try:
            WebDriverWait(self.browser, timeout=10).until(
                EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, '关闭')))
            self.browser.find_element_by_link_text('关闭').click()
            time.sleep(2)
        except:
            element_existance = False

        keyword = '国药准字H20'
        input_tag = self.browser.find_element_by_xpath('//*[@id="home"]/div[2]/div[7]/div/div[2]/input')
        input_tag.send_keys(keyword)
        element = self.browser.find_element_by_class_name('el-button.el-button--default')
        element.click()
        time.sleep(random.random() * 3)
        self.browser.get('https://www.nmpa.gov.cn/datasearch/search-result.html')
        time.sleep(random.random() * 3)
        self.browser.switch_to.window(self.browser.window_handles[-1])
        self.browser.close()
        time.sleep(random.random() * 3)
        self.browser.switch_to.window(self.browser.window_handles[0])
        onclock = "javascript:window.open('https://www.nmpa.gov.cn/datasearch/search-result.html')"
        # self.browser.execute_script(onclock)
        # 判断网页中是否存在跳过
        try:
            WebDriverWait(self.browser, timeout=10).until(
                EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, '跳过')))
            self.browser.find_element_by_link_text('跳过').click()
            time.sleep(2)
        except:
            element_existance = False

        keywordlist = ['H108', 'H1090', 'H1091', 'H1092', 'H1093', 'H1094', 'H1095', 'H1096', 'H1097', 'H1098',
                       'H1099', 'H11020', 'H11021', 'H11022', 'H12', 'H13020', 'H13021', 'H13022', 'H13023', 'H13024',
                       'H14020', 'H14021', 'H14022', 'H14023', 'H14024', 'H15', 'H1998', 'H19990', 'H19991',
                       'H19993', 'H19994', 'H19999', 'H21020', 'H21021', 'H21022', 'H21023', 'H21024', 'H22020',
                       'H22021', 'H22022', 'H22023',
                       'H22024', 'H22025', 'H22026',
                       'H23020', 'H23021', 'H23022', 'H23023', 'H2010', 'H2011', 'H2012', 'H2013', 'H2014', 'H2015',
                       'H2016', 'H2017',
                       'H2018', 'H2019', 'H2020', 'H2021',
                       'H2000', 'H2001', 'H2002', 'H2003', 'H20040', 'H20041', 'H20042', 'H20043', 'H20044', 'H20045',
                       'H20046',
                       'H20050', 'H20051', 'H20052', 'H20053', 'H20054', 'H20055', 'H20056', 'H20057', 'H20058',
                       'H20059',
                       'H20060', 'H20061', 'H20063', 'H20064', 'H20065', 'H20066', 'H20067', 'H20068', 'H2007',
                       'H20080', 'H20083', 'H20084', 'H2009', 'H31020', 'H31021', 'H31022', 'H31023', 'H32020',
                       'H32021', 'H32022', 'H32023', 'H32024', 'H32025',
                       'H32026',
                       'H33020', 'H33021', 'H33022', 'H34020', 'H34021', 'H34022', 'H34023', 'H34024', 'H35', 'H36',
                       'H37020', 'H37021', 'H37022', 'H37023', 'H37024',
                       'H50', 'H51020', 'H51021', 'H51022', 'H51023', 'H51024', 'H52', 'H53020', 'H53021', 'H53022',
                       'H54',
                       'H61', 'H62', 'H63', 'Z0',
                       'Z10', 'Z11', 'Z12', 'Z13020', 'Z13021', 'Z13022', 'Z14020', 'Z14021', 'Z15020', 'Z15021', 'Z19',
                       'Z2000', 'Z2001',
                       'Z20020', 'Z20023', 'Z20025', 'Z20026', 'Z20027', 'Z20028',
                       'Z2003', 'Z2004',
                       'Z20050', 'Z20053', 'Z20054', 'Z20055',
                       'Z2006', 'Z2007', 'Z2008', 'Z2009', 'Z201', 'Z202', 'Z21',
                       'Z22020', 'Z22021', 'Z22022', 'Z22023', 'Z22024', 'Z22025', 'Z22026',
                       'Z23',
                       'Z31', 'Z32', 'Z33', 'Z34', 'Z35', 'Z36', 'Z37',
                       'Z50', 'Z51020', 'Z51021', 'Z51022', 'Z52', 'Z53', 'Z54',
                       'Z61', 'Z62', 'Z63', 'Z64', 'Z65', 'Z41020', 'Z41021', 'Z41022', 'Z42020', 'Z42021', 'Z42022',
                       'Z43', 'Z44020', 'Z44021',
                       'Z44022', 'Z44023',
                       'Z45020', 'Z45021', 'Z45022', 'Z46',
                       'B', 'F', 'C', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6', ]

        keyword_page = '2'
        keyword_page1 = '1' #断点续爬设置页码
        # H1998:26
        k = 0  #断点续爬设置keywordlist里的列表元素位置
        for i in range(k, len(keywordlist) + 1):
            keyword = '国药准字{}'.format(keywordlist[i])
            print(keyword)
            input_keyword = self.browser.find_element_by_class_name(
                'el-input-group--append').find_element_by_class_name('el-input__inner')
            input_keyword.clear()
            input_keyword.send_keys(keyword)
            input_keyword.send_keys(Keys.ENTER)
            time.sleep(random.random() * 3)

            # 重置转跳页码
            input_page_tag = self.browser.find_element_by_xpath('//*[@id="home"]/div[3]/div[3]/div/span[3]/div/input')
            input_page_tag.clear()
            input_page_tag.send_keys(keyword_page)
            input_page_tag.send_keys(Keys.ENTER)
            time.sleep(random.random() * 3)
            input_page_tag.clear()
            time.sleep(random.random() * 3)

            # 双击事件
            ActionChains(self.browser).double_click(input_page_tag).perform()
            # 输入内容
            input_page_tag.send_keys(keyword_page1)
            input_page_tag.send_keys(Keys.ENTER)
            time.sleep(random.random() * 3)

            self.search_in_webpage(self.browser, keyword)
            keyword_page1 = '1'

    def search_in_webpage(self, browser, keyword):
        # 总页数
        pages = self.browser.find_element_by_class_name('el-pager').find_elements_by_class_name('number')[-1].text
        # pages = self.browser.find_element_by_xpath('//*[@id="home"]/div[3]/div[3]/div/ul/li[8]').text
        # pages=2
        print(pages)
        return_lists = []
        signal = True  # 执行循环信号
        while signal:
            return_lists = []

            page = browser.find_element_by_class_name('el-pager').find_element_by_class_name('active').text
            print(page)
            xiangqing_list = self.browser.find_elements_by_class_name('el-button--primary')

            for i in range(1, len(xiangqing_list) + 1):
                xpath_title = '//*[@id="home"]/div[3]/div[2]/div/div/div[3]/table/tbody/tr[{0}]/td[6]/div/button/span'.format(
                    i)

                browser.find_element_by_xpath(xpath_title).click()
                time.sleep(random.random() * 3)

                # WebDriverWait(self.browser, 10).until(self.browser.switch_to.window(self.browser.window_handles[-1]))

                browser.switch_to.window(browser.window_handles[-1])  # 将定位焦点切换到指定的窗口，包含所有可切换焦点的选项

                re_list = []
                re_list.append(page)

                try:
                    content = browser.find_element_by_xpath(
                        '//*[@id="dataTable"]/div[2]/table/tbody/tr[14]/td[2]/div/div/div').text
                except:
                    content = ''

                i = 0
                while content == '':
                    # print('数据为空')
                    browser.refresh()
                    time.sleep(2)
                    try:
                        content = browser.find_element_by_xpath(
                            '//*[@id="dataTable"]/div[2]/table/tbody/tr[14]/td[2]/div/div/div').text
                    except:
                        content = ''
                    i = i + 1
                    if i > 7:
                        break

                list_class = browser.find_elements_by_class_name('el-table_1_column_2')

                for i in list_class:
                    tilte = i.text
                    re_list.append(tilte)
                if len(re_list) < 17:
                    if len(re_list) == 1:
                        re_list.append(keyword)
                    else:
                        re_list[1] = keyword
                    for i in range(0, 17 - len(re_list)):
                        content = ''
                        re_list.append(content)
                print(re_list)
                browser.close()
                time.sleep(random.random() * 3)
                browser.switch_to.window(self.browser.window_handles[0])
                return_lists.append(re_list)

            if signal:

                if page == pages:
                    print('No next page!')
                    signal = False
                else:
                    self.browser.find_element_by_class_name('btn-next').click()
                    time.sleep(random.random() * 3)
            self.save_mysql(return_lists)
            print('成功写入数据库')

    def run(self):
        i = datetime.datetime.now()
        print("当前的日期和时间是 %s" % i)

        url = 'https://www.nmpa.gov.cn/datasearch/'
        # url = "http://httpbin.org/ip"
        print('开始爬取:', url)
        self.page_reset(url)

    # 数据库
    def save_mysql(self, content):
        # 数据库地址
        HOST = '124.70.83.178'
        # MySql端口
        MYSQL_PORT = 3308
        # MySQl用户名、密码
        MYSQL_USERNAME = 'industry'
        MYSQL_PASSWORD = 'Industry123!@#'
        # 数据库名
        SQL_NAME = 'industry_products'

        db = pymysql.connect(host=HOST, user=MYSQL_USERNAME, port=MYSQL_PORT, password=MYSQL_PASSWORD, db=SQL_NAME)
        cursor = db.cursor()

        sql = "CREATE TABLE IF NOT EXISTS drug_info (爬取页码 VARCHAR(255) NOT NULL,批准文号 VARCHAR(255) NOT NULL, 产品名称 VARCHAR(255) NOT NULL, 英文名称 VARCHAR(255) NOT NULL, 商品名 VARCHAR(255) NOT NULL, 剂型 VARCHAR(255) NOT NULL, 规格 VARCHAR(500) NOT NULL," \
              "上市许可持有人 VARCHAR(500) NOT NULL,上市许可持有人地址 VARCHAR(500) NOT NULL, 生产单位 VARCHAR(500) NOT NULL,批准日期 VARCHAR(255) NOT NULL, 生产地址 VARCHAR(500) NOT NULL, 产品类别 VARCHAR(255) NOT NULL, 原批准文号 VARCHAR(255) NOT NULL," \
              "药品本位码 VARCHAR(255) NOT NULL, 药品本位码备注 VARCHAR(500) NOT NULL,数据库相关备注 VARCHAR(500) NOT NULL)"

        cursor.execute(sql)
        value_title = ['爬取页码', '批准文号', '产品名称', '英文名称', '商品名', '剂型', '规格', '上市许可持有人',
                       '上市许可持有人地址', '生产单位', '批准日期', '生产地址', '产品类别', '原批准文号'
            , '药品本位码', '药品本位码备注', '数据库相关备注']

        tables = 'drug_info'
        keys = ','.join(value_title[0:len(value_title)])
        values = ','.join(['%s'] * len(value_title))

        sql2 = 'INSERT INTO {tables} ({keys}) VALUES({values})'.format(tables=tables, keys=keys, values=values)
        # cursor.execute(sql2, content)
        # db.commit()
        for i in content:
            cursor.execute(sql2, i)
            db.commit()


if __name__ == '__main__':
    Drug().run()





