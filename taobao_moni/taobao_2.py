"""
1 扫码登陆：操作简便，结果可直接使用
"""
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

options = Options()
a = webdriver.Chrome(
    executable_path='C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe', options=options)


class SessionException(Exception):
    def __init__(self, message):
        super().__init__(self)
        self.message = message

    def __str__(self):
        return self.message


class login():

    def __init__(self):
        self.browser = None
        self.wait = WebDriverWait(self.browser, 10)

    def start(self):
        self.__init__browser()
        self.browser.get('https://login.taobao.com/member/login.jhtml')
        self.browser.implicitly_wait(10)  # 智能等待，直到网页加载完毕，
        print('Please scan the qr code!')
        # 等待扫描二维码
        while True:
            qr_code = self.__is_element_exist('#J_QRCodeImg')  # 二维码是否存在
            login_button = self.__is_element_exist('.J_Submit')  # 登陆按钮是否存在
            serach_button = self.__is_element_exist('.btn-search.tb-bg')  # 登陆后搜索商品按钮是否存在
            # 二维码存在，登录按钮存在，登陆后的搜索商品按钮不存在，判定为扫码未完成，继续等待扫码
            if qr_code and login_button and not serach_button:
                continue
            else:
                break
            time.sleep(1)  # 每隔1s检测一次是否扫描二维码

        hp_btn = self.browser.find_element_by_xpath('//*[@id="J_SiteNavHome"]/div/a/span')
        if hp_btn:
            time.sleep(1)
            hp_btn.click()

    def __init__browser(self):
        """初始化浏览器"""
        options = Options()
        # options.add_argument("--headless")
        prefs = {"profile.managed_default_content_settings.images": 1}
        options.add_experimental_option("prefs", prefs)
        # options.add_argument('--proxy-server=http://127.0.0.1:9000')
        options.add_argument('disable-infobars')
        options.add_argument('--no-sandbox')

        self.browser = webdriver.Chrome(
            executable_path='C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe', options=options)
        self.browser.implicitly_wait(3)
        self.browser.maximize_window()

    def __is_element_exist(self, selector):
        """检查是否存在指定元素"""
        try:
            self.browser.find_element_by_css_selector(selector)
            return True
        except NoSuchElementException:
            return False


if __name__ == '__main__':
    cookie = login().start()
    print(cookie)
