import time,pymysql
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class Drug(object):

    def __init__(self):
        # 声明一个谷歌驱动器，并设置不加载图片，间接加快访问速度
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # 如何实现让selenium规避被检测的风险
        #self.options.add_argument('headless')  # 设置option
        # self.options.add_argument("window-size=1400,600")\
        self.options.add_argument("--disable-blink-features=AutomationControlled")

        self.options.add_argument("--incognito")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--disable-dev-shm-usage")
        # self.options.AddArguments("--incognito", "--disable-blink-features=AutomationControlled")
        self.options.add_argument(
            'user-agent="Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19"')
        self.options.add_experimental_option('prefs', {'profile.managed_default_content_settings.images': 2})

        self.options.add_experimental_option('useAutomationExtension', False)
        self.browser = webdriver.Chrome(chrome_options=self.options, port=9020)
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

    def page_reset(self,url):
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

        keyword = '皖械注准'
        input_tag = self.browser.find_element_by_xpath('//*[@id="home"]/div[2]/div[7]/div/div[2]/input')
        input_tag.send_keys(keyword)
        element = self.browser.find_element_by_class_name('el-button.el-button--default')
        element.click()
        time.sleep(2)
        self.browser.get('https://www.nmpa.gov.cn/datasearch/search-result.html')
        time.sleep(2)
        self.browser.switch_to.window(self.browser.window_handles[-1])
        self.browser.close()
        time.sleep(2)
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


        keywordlist =  ['皖械注准201','皖械注准202','鲁械注准2014','鲁械注准2015','鲁械注准2016','鲁械注准2017','鲁械注准2018','鲁械注准2019','鲁械注准202',
           '新械注准','苏械注准2014','苏械注准2015','苏械注准2016','苏械注准2017','苏械注准2018','苏械注准2019','苏械注准2020','苏械注准2021',
           '赣械注准201','赣械注准202','鄂械注准201','鄂械注准202','桂械注准','甘械注准','晋械注准','内械注准','陕械注准','吉械注准','闽械注准',
           '黔械注准','青械注准','藏械注准','宁械注准','川械注准','琼械注准','兵械注准','浙械注准2014','浙械注准2015','浙械注准2016','浙械注准2017',
           '浙械注准2018','浙械注准2019','浙械注准202','粤械注准2014','粤械注准2015','粤械注准2016','粤械注准2017','粤械注准2018','粤械注准2019',
           '粤械注准2020','粤械注准2021','国械注准202','国械注准2014','国械注准2015','国械注准2016','国械注准2017','国械注准2018','国械注准2019']


        keyword_page = '2'
        keyword_page1='1' #断点续爬设置页码
        k = 0  # 断点续爬设置keywordlist里的列表元素位置
        for i in range(k, len(keywordlist)+1):
            keyword='{0}'.format(keywordlist[i])
            print(keyword)
            input_keyword = self.browser.find_element_by_class_name(
                'el-input-group--append').find_element_by_class_name('el-input__inner')
            input_keyword.clear()
            input_keyword.send_keys(keyword)
            input_keyword.send_keys(Keys.ENTER)
            time.sleep(2)

            # 重置转跳页码

            input_page_tag = self.browser.find_element_by_xpath('//*[@id="home"]/div[3]/div[3]/div/span[3]/div/input')
            input_page_tag.clear()
            input_page_tag.send_keys(keyword_page)
            input_page_tag.send_keys(Keys.ENTER)
            time.sleep(2)
            input_page_tag.clear()
            time.sleep(2)

            # 双击事件
            ActionChains(self.browser).double_click(input_page_tag).perform()
            # 输入内容
            input_page_tag.send_keys(keyword_page1)
            input_page_tag.send_keys(Keys.ENTER)
            time.sleep(2)

            self.search_in_webpage(self.browser,keyword)
            keyword_page1 = '1'

    def search_in_webpage(self,browser,keyword):
        # 总页数
        pages=self.browser.find_element_by_class_name('el-pager').find_elements_by_class_name('number')[-1].text
        #pages = self.browser.find_element_by_xpath('//*[@id="home"]/div[3]/div[3]/div/ul/li[8]').text
        # pages=2
        print(pages)
        return_lists = []
        signal = True  # 执行循环信号
        while signal:
            return_lists = []

            page = browser.find_element_by_class_name('el-pager').find_element_by_class_name('active').text
            print(page)
            xiangqing_list = self.browser.find_elements_by_class_name('el-button--primary')

            for i in range(1, len(xiangqing_list)+1):
                xpath_title = '//*[@id="home"]/div[3]/div[2]/div/div/div[3]/table/tbody/tr[{0}]/td[5]/div/button/span'.format(i)

                browser.find_element_by_xpath(xpath_title).click()
                time.sleep(2)

                #WebDriverWait(self.browser, 10).until(self.browser.switch_to.window(self.browser.window_handles[-1]))

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
                    #print('数据为空')
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


                list_class = browser.find_elements_by_class_name('el-table_1_column_2.is-left ')

                for i in list_class:
                    tilte = i.text
                    re_list.append(tilte)

                if len(re_list)<19:
                    if len(re_list) == 1:
                        re_list.append(keyword)
                    else:
                        re_list[1] = keyword
                    for i in range(0,19-len(re_list)):
                        content = ''
                        re_list.append(content)
                print(re_list)
                browser.close()
                time.sleep(2)
                browser.switch_to.window(self.browser.window_handles[0])
                return_lists.append(re_list)

            if signal:

                if page == pages:
                    print('No next page!')
                    signal = False
                else:
                    self.browser.find_element_by_class_name('btn-next').click()
                    time.sleep(4)
            self.save_mysql(return_lists)
            print('成功写入数据库')

    def run(self):
        i = datetime.datetime.now()
        print("当前的日期和时间是 %s" % i)

        url = url = 'https://www.nmpa.gov.cn/datasearch/home-index.html#category=ylqx'
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

        sql = "CREATE TABLE IF NOT EXISTS Medical_Devices_info1 (爬取页码 VARCHAR(255) NOT NULL,注册证编号 VARCHAR(255) NOT NULL, 注册人名称 VARCHAR(255) NOT NULL, 注册人住所 VARCHAR(255) NOT NULL, 生产地址 VARCHAR(255) NOT NULL, 产品名称 VARCHAR(255) NOT NULL, 管理类别 VARCHAR(500) NOT NULL," \
              "型号规格 text NOT NULL,结构及组成或主要组成成分 text NOT NULL, 适用范围或预期用途 text NOT NULL,产品储存条件及有效期 text NOT NULL, 附件 VARCHAR(500) NOT NULL, 其他内容 text NOT NULL, 备注 text NOT NULL," \
              "审批部门 VARCHAR(255) NOT NULL, 批准日期 VARCHAR(500) NOT NULL,有效期至 VARCHAR(500) NOT NULL,变更情况 text NOT NULL,数据库相关备注 text NOT NULL)"

        cursor.execute(sql)

        value_title = ['爬取页码', '注册证编号', '注册人名称', '注册人住所', '生产地址', '产品名称', '管理类别', '型号规格',
                        '结构及组成或主要组成成分', '适用范围或预期用途', '产品储存条件及有效期', '附件', '其他内容',
                        '备注', '审批部门', '批准日期', '有效期至', '变更情况', '数据库相关备注']

        tables = 'Medical_Devices_info1'
        keys = ','.join(value_title[0:len(value_title)])
        values = ','.join(['%s'] * len(value_title))

        sql2 = 'INSERT INTO {tables} ({keys}) VALUES({values})'.format(tables=tables, keys=keys, values=values)
        #cursor.execute(sql2, content)
        #db.commit()
        for i in content:
            cursor.execute(sql2, i)
            db.commit()

if __name__ == '__main__':
    Drug().run()