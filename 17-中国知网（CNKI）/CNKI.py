import requests
from bs4 import BeautifulSoup
import urllib.parse
import json
import re

requests.packages.urllib3.disable_warnings()

# 使用学校ip登录的cookie可以下载文献
# 直接ip登录后需要过一个验证码才是可以下载文献的cookie
COOKIE = 'Ecp_notFirstLogin=0DCqVE; Ecp_ClientId=1200801090700543834; RsPerPage=20; cnkiUserKey=5aa0e831-eda6-0b84-22a8-d8d8eef7c850; _pk_ref=%5B%22%22%2C%22%22%2C1604134169%2C%22https%3A%2F%2Fwww.cnki.net%2F%22%5D; Ecp_ClientIp=183.134.202.250; Ecp_loginuserbk=DX0434; _pk_ref=%5B%22%22%2C%22%22%2C1619365155%2C%22https%3A%2F%2Fwww.google.com.hk%2F%22%5D; _pk_ses=*; c_m_LinID=LinID=WEEvREcwSlJHSldSdmVqMDh6a1dpb2RtaHpmRmpwTTA4ZEJiSXNIZWRCQT0=$9A4hF_YAuvQ5obgVAqNKPCYcEjKensW4IQMovwHtwkF4VYPoHbKxJw!!&ot=05/02/2021 23:43:48; LID=WEEvREcwSlJHSldSdmVqMDh6a1dpb2RtaHpmRmpwTTA4ZEJiSXNIZWRCQT0=$9A4hF_YAuvQ5obgVAqNKPCYcEjKensW4IQMovwHtwkF4VYPoHbKxJw!!; c_m_expire=2021-05-02 23:43:48; Ecp_session=1; Ecp_LoginStuts={"IsAutoLogin":false,"UserName":"DX0434","ShowName":"%E6%B5%99%E6%B1%9F%E7%90%86%E5%B7%A5%E5%A4%A7%E5%AD%A6","UserType":"bk","BUserName":"","BShowName":"","BUserType":"","r":"0DCqVE"}; ASP.NET_SessionId=c2rcveqsdiwgd14smq5ethux; SID_kns8=123117; CurrSortField=%e5%8f%91%e8%a1%a8%e6%97%b6%e9%97%b4%2f(%e5%8f%91%e8%a1%a8%e6%97%b6%e9%97%b4%2c%27TIME%27); CurrSortFieldType=desc; SID_kns_new=kns123124; _pk_id=5b33d458-abb7-4088-be29-7e9573c36da5.1612013968.5.1619365483.1619365155.'


def download_paper(url, saved_name):
    payload = {}
    # 注意请求头中不能加host否则将请求不到文件原因未知
    # 使用nodejs 的superagent库加host也可以请求到文件
    headers = {
        # 'Host': 'kns.cnki.net',# 这个字段不能加 
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en;q=0.7',
        'Cookie': COOKIE
    }
    response = requests.get(url, headers=headers, data=payload, verify=False)
    print(response.headers)
    if response.headers['Content-Type'] == 'application/caj':
        with open(saved_name + '.caj', 'wb') as f:
            f.write(response.content)
            f.close()
    else:
        raise Exception("cookie 过期")


def get_detail(all_params):
    url = "https://kns.cnki.net/KNS8/Brief/GetGridTableHtml"
    QueryJson = {
        "Platform": "",
        "DBCode": "SCDB",
        "KuaKuCode": "CJFQ,CDMD,CIPD,CCND,CISD,SNAD,BDZK,CCVD,CJFN,CCJD",
        "QNode": {
            "QGroup": all_params["QGroup"]
        }
    }
    # print(urllib.parse.quote(json.dumps(QueryJson)))  # payload = "IsSearch=true&QueryJson=%7B%22Platform%22%3A%22%22%2C%22DBCode%22%3A%22SCDB%22%2C%22KuaKuCode%22%3A%22CJFQ%2CCDMD%2CCIPD%2CCCND%2CCISD%2CSNAD%2CBDZK%2CCCVD%2CCJFN%2CCCJD%22%2C%22QNode%22%3A%7B%22QGroup%22%3A%5B%7B%22Key%22%3A%22Subject%22%2C%22Title%22%3A%22%22%2C%22Logic%22%3A1%2C%22Items%22%3A%5B%7B%22Title%22%3A%22%E4%B8%BB%E9%A2%98%22%2C%22Name%22%3A%22SU%22%2C%22Value%22%3A%22java%22%2C%22Operate%22%3A%22%25%3D%22%2C%22BlurType%22%3A%22%22%7D%5D%2C%22ChildItems%22%3A%5B%5D%7D%5D%7D%7D&SearchSql=&PageName=DefaultResult&HandlerId=0&DBCode=SCDB&KuaKuCodes=CJFQ%2CCDMD%2CCIPD%2CCCND%2CCISD%2CSNAD%2CBDZK%2CCCVD%2CCJFN%2CCCJD&CurPage=1&RecordsCntPerPage=20&CurDisplayMode=listmode&CurrSortField=%25e5%258f%2591%25e8%25a1%25a8%25e6%2597%25b6%25e9%2597%25b4%252f(%25e5%258f%2591%25e8%25a1%25a8%25e6%2597%25b6%25e9%2597%25b4%252c%2527TIME%2527)&CurrSortFieldType=desc&IsSortSearch=false&IsSentenceSearch=false&Subject="
    payload = f"IsSearch=true&QueryJson={urllib.parse.quote(json.dumps(QueryJson))}&SearchSql=&PageName=DefaultResult&HandlerId=0&DBCode=SCDB&KuaKuCodes=CJFQ%2CCDMD%2CCIPD%2CCCND%2CCISD%2CSNAD%2CBDZK%2CCCVD%2CCJFN%2CCCJD&CurPage={all_params['page']}&RecordsCntPerPage=20&CurDisplayMode=listmode&CurrSortField=%25e5%258f%2591%25e8%25a1%25a8%25e6%2597%25b6%25e9%2597%25b4%252f(%25e5%258f%2591%25e8%25a1%25a8%25e6%2597%25b6%25e9%2597%25b4%252c%2527TIME%2527)&CurrSortFieldType=desc&IsSortSearch=false&IsSentenceSearch=false&Subject="
    headers = {
        'Accept': 'text/html, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://kns.cnki.net',
        'Referer': 'https://kns.cnki.net/kns8/defaultresult/index',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en;q=0.7',
        'Cookie': COOKIE
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
            print(name, downloadlink)
            try:
                download_paper(downloadlink, name)
            except Exception as e:
                print(e)


if __name__ == '__main__':
    for page in range(1, 99):
        print("-" * 20 + '  page:', page, "   " + '-' * 20)
        all_params = {
            'page': str(page),
            'QGroup': [{
                "Key": "Subject",
                "Title": "",
                "Logic": 1,
                "Items": [{
                    "Title": "主题",
                    "Name": "SU",
                    "Value": "光子晶体",
                    "Operate": "%=",
                    "BlurType": ""
                }],
                "ChildItems": []
            }]
        }
        get_detail(all_params)
