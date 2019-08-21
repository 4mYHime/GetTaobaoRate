import requests
import time
import json

session = requests.session()


# 获取商品ID
def get_id_json(page, keyword):
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'referer': 'https://uland.taobao.com/semm/tbsearch?refpid=mm_26632258_3504122_32554087&keyword=%E5%A5%B3%E8'
                   '%A3%85 '
                   '&rewriteQuery=1&a=mi={imei}&sms=baidu&idfa={'
                   'idfa}&clk1=abab6283306413775910d4b0b37ca047&upsid=abab6283306413775910d4b0b37ca047',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/%s Mobile Safari/537.36',
    }
    url = 'https://odin.re.taobao.com/m/Nwalltbuad?sbid=sem2_kgb_activity&ignore=CATID%2CRANKINFO%2CMATCHTYPE&pvid=_TL' \
          '-41832&refpid=mm_26632258_3504122_32554087&clk1=abab6283306413775910d4b0b37ca047&idfa=%7Bidfa%7D&pid' \
          '=430680_1006&keyword=' + keyword + '&count=60&offset=' + str(60 * page) + '&relacount=8&t=1535075213992' \
                                                                                     '&callback' \
                                                                                     '=mn17jsonp1535075213992 '
    r = session.get(url=url, headers=headers)
    html = r.text
    start = html.find('(')
    datas = (json.loads(html[start + 1:-1]))['result']['item']
    return datas


# 获取评论，通过携带登录过后的cookie
def getCommentByCookie(resource_id):
    url = "https://rate.taobao.com/feedRateList.htm?auctionNumId=" + resource_id + "&currentPageNum=10&pageSize=20"
    headers = {
        "cookie": "v=0; t=8fb7ca8a45fe2057fd4159410fa830f8; cookie2=1b18c56600360e795789fa6c58ad5529; _tb_token_=f75eef3e73341; l=cB_-DD6VqiB-4svEKOfZKurza77t6IObzsPzaNbMiICPOMX6S91OWZeZmX-BCnGVLsLW837uMFCUBVToRPU65Wrr2D_7XPQl.; isg=BAYG-34-p0s1kHMm4yTFeksUV_yIZ0oh1lyp6PAtsCkr86MNXfNlMWDBy2-a20I5",
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
        'Connection': 'keep-alive'
    }

    r = session.get(url, headers=headers)
    r.raise_for_status()
    r.encoding = 'utf-8'
    try:
        # 评论数
        total = json.loads(r.text.strip().strip('()'))['total']
        count = 0
        page = 1
        while count < total:
            url = "https://rate.taobao.com/feedRateList.htm?auctionNumId=" + resource_id + "&currentPageNum=" + str(
                page) + "&pageSize=20"
            r = session.get(url=url, headers=headers)
            page = page + 1
            comments = json.loads(r.text.strip().strip('()'))['comments']
            for comment in comments:
                print(comment)
                count = count + 1
            time.sleep(5)
    except Exception as e:
        print(e)


# 获取评论，不携带cookie，此方法
def getComment(resource_id):
    url = "https://rate.taobao.com/feedRateList.htm?auctionNumId=" + resource_id + "&currentPageNum=10&pageSize=20"
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0'
    }
    session.headers = headers

    r = session.head(url=url, allow_redirects=True)
    print(r.headers)
    print(r.status_code)
    print(r.history)

    html_set_cookie = requests.utils.dict_from_cookiejar(session.cookies)
    r = session.get(url=url, cookies=html_set_cookie)
    print(r.request.headers)
    print(r.text)


def getJsonData(page, keyword):
    for item in range(0, page):
        datas = get_id_json(page + 1, keyword)
        for item in datas:
            resource_id = item["RESOURCEID"]
            getCommentByCookie(resource_id)
            getComment(resource_id)


if __name__ == "__main__":
    page = 10
    keyword = "iphone x".replace(" ", "+")
    getJsonData(page, keyword)
