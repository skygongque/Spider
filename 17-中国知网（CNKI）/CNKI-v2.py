import requests
from bs4 import BeautifulSoup
import urllib.parse
import json
import re
from retrying import retry
requests.packages.urllib3.disable_warnings()

""" 
知网文献批量下载
1.支持按被引排序并筛选近5年后开始下载
2.调用接口实现验证码识别，可自己在本地搭建验证码的识别服务
"""



# 全程使用session 保存回话
sess = requests.session()

default_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Referer': 'https://www.cnki.net/'
}


def login(sess):
    response = sess.get(
        "https://login.cnki.net/TopLoginNew/api/loginapi/IpLogin?isAutoLogin=true&checkCode=&isForceLogin=true&p=2&vc=%7C0&_=1625586211994", headers=default_headers, verify=False)
    print(response.text)
    return sess


def loginOut(sess):
    response = sess.post(
        'https://kns.cnki.net/KNS8/login/LoginOut?q=-1', headers=default_headers)
    print(response.text)


def recognizeCaptcha(sess, referer):
    """ 调用接口识别验证码 
    https://github.com/sml2h3/captcha_server
    """
    resp = sess.get(
        'https://kdoc.cnki.net/kdoc/request/ValidateCode.ashx?t=1625499833480', headers=default_headers, verify=False)
    captcha_img = resp.content
    # # 识别
    resp = requests.post("http://127.0.0.1:9898/api",
                         files={'image': captcha_img})
    # 保存验证码用于查看
    with open('captcha.jpg', 'wb') as f:
        f.write(captcha_img)
    print('验证码结果', resp.text)
    return resp.text


def getRedirectUrl(url: str, sess: object) -> str:
    """ 获取重定向的location """
    response = sess.get(url, headers=default_headers,
                        verify=False, allow_redirects=False)
    return dict(response.headers).get("Location")


def postDownloadUrl(url, sess, vcode, referer, name_saved):
    """
    验证码识别成功直接开始下载 caj 文件 return None
    识别失败 return '验证码错误'
    """
    payload = f'vcode={str(vcode)}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': referer,
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Origin': 'https://kdoc.cnki.net',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = sess.post(url, headers=headers, data=payload)
    if response.headers['Content-Type'] == 'application/caj':
        with open(f'{name_saved}.caj', 'wb') as f:
            f.write(response.content)
            f.close()
        return None
    else:
        print(response.text)
        return '验证码错误'


def saveCaptcha(url, sess, referer):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': referer,
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    response = sess.get(url, headers=headers)
    with open('currentCaptcha.jpg', 'wb') as f:
        f.write(response.content)
        f.close()


@retry
def download_paper(url, saved_name, sess):
    """ 下载一篇文献 """
    response = sess.get(url, headers=default_headers)
    # print(response.headers)
    if response.headers['Content-Type'] == 'application/caj':
        with open(saved_name + '.caj', 'wb') as f:
            f.write(response.content)
            f.close()
        print(f'[Downloaded] {saved_name}.caj successfully')
    elif '验证码' in response.text:
        redirectUrl = getRedirectUrl(url, sess)
        # saveCaptcha(
        #     'https://kdoc.cnki.net/kdoc/request/ValidateCode.ashx?t=1577242936454', sess, redirectUrl)
        # vcode = input('输入验证码:')
        vcode = recognizeCaptcha(sess, redirectUrl)
        iswrongCaptcha = postDownloadUrl(
            redirectUrl, sess, vcode, redirectUrl, saved_name)
        while iswrongCaptcha:
            # 验证码识别错误的情况
            vcode = recognizeCaptcha(sess, redirectUrl)
            iswrongCaptcha = postDownloadUrl(
                redirectUrl, sess, vcode, redirectUrl, saved_name)
    elif "对不起，您的操作太过频繁！请退出后重新登录。" in response.text:
        print(response.text)
        # sess = loginOut(sess)
        # 重新登录操作
        sess = requests.session()
        sess = login(sess)
        redirectUrl = getRedirectUrl(url, sess)
        # saveCaptcha(
        #     'https://kdoc.cnki.net/kdoc/request/ValidateCode.ashx?t=1577242936454', sess, redirectUrl)
        # vcode = input('输入验证码:')
        vcode = recognizeCaptcha(sess, redirectUrl)
        iswrongCaptcha = postDownloadUrl(
            redirectUrl, sess, vcode, redirectUrl, saved_name)
        while iswrongCaptcha:
            vcode = recognizeCaptcha(sess, redirectUrl)
            iswrongCaptcha = postDownloadUrl(
                redirectUrl, sess, vcode, redirectUrl, saved_name)
    else:
        print('=================其他情况=======================')
        print(response.text)
    # 可能已经重新登录 返回sess
    return sess


def get_detail(sess, QueryJson, sortParams):
    """ 下载一页文献 """
    url = "https://kns.cnki.net/KNS8/Brief/GetGridTableHtml"
    # print(urllib.parse.quote(json.dumps(QueryJson)))  # payload = "IsSearch=true&QueryJson=%7B%22Platform%22%3A%22%22%2C%22DBCode%22%3A%22SCDB%22%2C%22KuaKuCode%22%3A%22CJFQ%2CCDMD%2CCIPD%2CCCND%2CCISD%2CSNAD%2CBDZK%2CCCVD%2CCJFN%2CCCJD%22%2C%22QNode%22%3A%7B%22QGroup%22%3A%5B%7B%22Key%22%3A%22Subject%22%2C%22Title%22%3A%22%22%2C%22Logic%22%3A1%2C%22Items%22%3A%5B%7B%22Title%22%3A%22%E4%B8%BB%E9%A2%98%22%2C%22Name%22%3A%22SU%22%2C%22Value%22%3A%22java%22%2C%22Operate%22%3A%22%25%3D%22%2C%22BlurType%22%3A%22%22%7D%5D%2C%22ChildItems%22%3A%5B%5D%7D%5D%7D%7D&SearchSql=&PageName=DefaultResult&HandlerId=0&DBCode=SCDB&KuaKuCodes=CJFQ%2CCDMD%2CCIPD%2CCCND%2CCISD%2CSNAD%2CBDZK%2CCCVD%2CCJFN%2CCCJD&CurPage=1&RecordsCntPerPage=20&CurDisplayMode=listmode&CurrSortField=%25e5%258f%2591%25e8%25a1%25a8%25e6%2597%25b6%25e9%2597%25b4%252f(%25e5%258f%2591%25e8%25a1%25a8%25e6%2597%25b6%25e9%2597%25b4%252c%2527TIME%2527)&CurrSortFieldType=desc&IsSortSearch=false&IsSentenceSearch=false&Subject="
    payload = f"IsSearch={sortParams['IsSearch']}&QueryJson={urllib.parse.quote(json.dumps(QueryJson))}&SearchSql=&PageName=DefaultResult&HandlerId=0&DBCode=SCDB&KuaKuCodes=CJFQ%2CCDMD%2CCIPD%2CCCND%2CCISD%2CSNAD%2CBDZK%2CCCVD%2CCJFN%2CCCJD&CurPage={QueryJson['page']}&RecordsCntPerPage=20&CurDisplayMode=listmode&CurrSortField={sortParams['CurrSortField']}&CurrSortFieldType=desc&IsSortSearch={sortParams['IsSortSearch']}&IsSentenceSearch=false&Subject="
    headers = {
        'Accept': 'text/html, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://kns.cnki.net',
        'Referer': 'https://kns.cnki.net/kns8/defaultresult/index',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en;q=0.7',
        # 'Cookie': COOKIE
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    soup = BeautifulSoup(response.text, 'lxml')
    result_table_list = soup.select('.result-table-list')[0]
    trs = result_table_list.select('tr')[1:]
    for tr in trs:
        name = tr.select('.name > a')[0].get_text().strip()
        name = re.sub('[\/*?<>|]', ' ', name)
        downloadlink = tr.select('.downloadlink')
        if downloadlink != []:
            downloadlink = 'https://kns.cnki.net' + downloadlink[0]['href']
            # print(name, downloadlink)
            print(f'[info] start downloading {name}')
            # try:
            sess = download_paper(downloadlink, name, sess)
            # except Exception as e:
            #     print(e)
        else:
            pass
            # 知网没有下载链接的部分
        # break


if __name__ == '__main__':
    # ip登录
    sess = login(sess)
    QueryJson = {
        "Platform": "",
        "DBCode": "SCDB",
        "KuaKuCode": "CJFQ,CDMD,CIPD,CCND,CISD,SNAD,BDZK,CCVD,CJFN,CCJD",
        "QNode": {
            "QGroup": [{
                "Key": "Subject",
                "Title": "",
                "Logic": 1,
                "Items": [{
                    "Title": "主题",
                    "Name": "SU",
                    # 关键词
                    "Value": "聚乳酸",
                    "Operate": "%=",
                    "BlurType": ""
                }],
                # 筛选最近5年 不需筛选 "ChildItems" 为 []
                "ChildItems": [
                    {
                        "Key": "3",
                        "Title": "",
                        "Logic": 1,
                        "Items": [
                            {
                                "Key": "2021",
                                "Title": "2021",
                                "Logic": 2,
                                "Name": "年",
                                "Operate": "",
                                "Value": "2021",
                                "ExtendType": 0,
                                "ExtendValue": "",
                                "Value2": "",
                                "BlurType": ""
                            },
                            {
                                "Key": "2020",
                                "Title": "2020",
                                "Logic": 2,
                                "Name": "年",
                                "Operate": "",
                                "Value": "2020",
                                "ExtendType": 0,
                                "ExtendValue": "",
                                "Value2": "",
                                "BlurType": ""
                            },
                            {
                                "Key": "2019",
                                "Title": "2019",
                                "Logic": 2,
                                "Name": "年",
                                "Operate": "",
                                "Value": "2019",
                                "ExtendType": 0,
                                "ExtendValue": "",
                                "Value2": "",
                                "BlurType": ""
                            },
                            {
                                "Key": "2018",
                                "Title": "2018",
                                "Logic": 2,
                                "Name": "年",
                                "Operate": "",
                                "Value": "2018",
                                "ExtendType": 0,
                                "ExtendValue": "",
                                "Value2": "",
                                "BlurType": ""
                            },
                            {
                                "Key": "2017",
                                "Title": "2017",
                                "Logic": 2,
                                "Name": "年",
                                "Operate": "",
                                "Value": "2017",
                                "ExtendType": 0,
                                "ExtendValue": "",
                                "Value2": "",
                                "BlurType": ""
                            },
                            {
                                "Key": "2016",
                                "Title": "2016",
                                "Logic": 2,
                                "Name": "年",
                                "Operate": "",
                                "Value": "2016",
                                "ExtendType": 0,
                                "ExtendValue": "",
                                "Value2": "",
                                "BlurType": ""
                            },
                            {
                                "Key": "2015",
                                "Title": "2015",
                                "Logic": 2,
                                "Name": "年",
                                "Operate": "",
                                "Value": "2015",
                                "ExtendType": 0,
                                "ExtendValue": "",
                                "Value2": "",
                                "BlurType": ""
                            }
                        ],
                        "ChildItems": []
                    }
                ],
                # "ChildItems": []
            }]
        }
    }
    # 时间排序
    # sortParams = {
    #     'IsSearch': 'true',
    #     'CurrSortField': '%e5%8f%91%e8%a1%a8%e6%97%b6%e9%97%b4%2f(%e5%8f%91%e8%a1%a8%e6%97%b6%e9%97%b4%2c%27TIME%27)',
    #     'CurrSortFieldType': 'desc',
    #     'IsSortSearch': 'false'
    # }
    # 按被引排序
    sortParams = {
        'IsSearch': 'false',
        'CurrSortField': urllib.parse.quote("被引/(被引频次,'integer')"),
        'CurrSortFieldType': 'desc',
        'IsSortSearch': 'true'
    }
    # 爬取99页
    for page in range(1, 99):
        print("-" * 20 + '  page:', page, "   " + '-' * 20)
        QueryJson['page'] = str(page)
        get_detail(sess, QueryJson, sortParams)
        # break
