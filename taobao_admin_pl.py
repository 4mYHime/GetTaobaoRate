"""
该版本是针对登录到商家后台之后，抓取历史评价记录
"""

import time
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

options = Options()
browser = webdriver.Chrome(executable_path='C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe',
                           options=options)

# 扫码直接登陆到商家后台
browser.get('https://login.taobao.com/member/login.jhtml')
browser.implicitly_wait(10)


def __is_element_exist(selector):
    """检查是否存在指定元素"""
    try:
        browser.find_element_by_css_selector(selector)
        return True
    except NoSuchElementException:
        return False


aa = pd.DataFrame(data=[], columns=['买家', '评价内容', '图片', '时间', '客服回复', '商品抬头', '价格', '追加评论', '追加评论时间'])
aa.to_csv('result.csv')

print('Please scan the qr code!')
# 等待扫描二维码
while True:
    qr_code = __is_element_exist('#J_QRCodeImg')  # 二维码是否存在
    login_button = __is_element_exist('.J_Submit')  # 登陆按钮是否存在
    serach_button = __is_element_exist('.btn-search.tb-bg')  # 登陆后搜索商品按钮是否存在
    # 二维码存在，登录按钮存在，登陆后的搜索商品按钮不存在，判定为扫码未完成，继续等待扫码
    if qr_code and login_button:
        continue
    else:
        break
    time.sleep(1)  # 每隔1s检测一次是否扫描二维码

# 开始工作
# 定位并点击【评价管理】按钮
rate_manage_button = browser.find_element_by_xpath('//*[@id="J_SelectMenu"]/div[2]/ul/li[2]/span/a')
rate_manage_button.click()
time.sleep(0.5)

while True:
    # 保存评价数据
    rate_data_elements = browser.find_element_by_xpath('//*[@id="J_RateList"]')
    rate_data_element_list = rate_data_elements.find_elements_by_tag_name('tr')
    for rate_element in rate_data_element_list[1:]:
        # 保存字段
        # first_comment
        # first_photos []
        # reply
        # first_date
        # buyer_name
        # good_title
        # price
        # append_content
        # append_date
        time.sleep(0.1)
        elements = rate_element.find_elements_by_tag_name('td')
        # 评价信息
        first_rate_element = elements[0]
        if not first_rate_element:
            first_comment = None
            first_photos = None
            reply = None
            first_date = None
            append_content = None
            append_date = None
        else:
            first_comment = first_rate_element.find_element_by_class_name('comment').text
            first_date = first_rate_element.find_elements_by_class_name('date')[0].text
            try:
                reply = first_rate_element.find_element_by_class_name('reply').text
            except NoSuchElementException:
                reply = None
            try:
                first_photos_element = first_rate_element.find_element_by_class_name('photos')
                if not first_photos_element:
                    first_photos = []
                else:
                    first_photos = [i.find_element_by_tag_name('a').get_attribute("href") for i in
                                    first_photos_element.find_elements_by_tag_name('li')]
            except NoSuchElementException:
                first_photos = []

            append_element = first_rate_element.find_elements_by_class_name('append')
            if not append_element:
                append_content = None
                append_date = None
            else:
                append_content = append_element[0].find_element_by_class_name('comment').text
                append_date = first_rate_element.find_elements_by_class_name('date')[1].text
        # 买家信息
        buyer_element = elements[1]
        buyer_name = buyer_element.find_element_by_tag_name('a').text

        good_info_element = elements[2]
        good_title = good_info_element.find_element_by_tag_name('a').get_attribute("title")
        price = good_info_element.find_element_by_tag_name('div').find_element_by_tag_name('em').text

        source_data = [buyer_name, first_comment, json.dumps(first_photos), first_date, reply, good_title, price, append_content, append_date]
        df1 = pd.DataFrame(data=[source_data], columns=['买家', '评价内容', '图片', '时间', '客服回复', '商品抬头', '价格', '追加评论', '追加评论时间'])
        df1.to_csv('result.csv', mode='a', header=False)
        time.sleep(0.5)
        print('=' * 10, '写入完成')
    # 定位页码栏
    page_bars = browser.find_element_by_xpath('//*[@id="rateList"]/div')
    page_links = page_bars.find_elements_by_tag_name('li')
    try:
        next_href = page_links[-1].find_element_by_tag_name('a').get_attribute('href')
    except NoSuchElementException:
        next_href = None
    if not next_href:
        break
    page_links[-1].click()
    continue
print("COMPLETE!")
