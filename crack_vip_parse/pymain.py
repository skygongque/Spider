import requests
import json
import hashlib
import time


def got(text):
    return hashlib.md5((text + "daheiyun1888").encode()).hexdigest()

def get_token(text):
    return hashlib.md5((text + "_wp6f").encode()).hexdigest()

def get_payload(url):
    key2 = '967642c7859c07c7032de44d20fb5bd5'
    tm = str(int(time.time()))
    key = got(got(url + tm + "daheiyunjiexi0614"))
    payload = {
        'url': url,
        'type': "",
        'ref': "0",
        'lg': "3",
        'tm': tm,
        'key': key,
        'key2': key2,
        'token': get_token(key),
        'sdky': get_token(tm)
    }
    return payload

def get_src(url):
    payload = get_payload(url)
    api = "http://jiexi.shunyiwenxiu.com/dhyjx_ver_9.1.php"
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'http://jiexi.shunyiwenxiu.com', 
        'Referer': f'http://jiexi.shunyiwenxiu.com/?url={url}&lg=3&key={payload["key"]}&tm={payload["tm"]}',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en;q=0.7',
        'Cookie': 'time_//api.adinisp.com/ximu-9426c06e139254993a407601a15571b4.m3u8=1645.14513; domain=jiexi.shunyiwenxiu.com; time_//api.adinisp.com/ximu-6bba361eb5299c55d5c7188fd1fe2ff9.m3u8=8.768052; sky_pm=33b065aa4aa42028512ce89971773439_1594911326656; sky_pm_en=1632d5220ca4fa6c7a365cff234927cf'
    }
    response = requests.request("POST", api, headers=headers, data=payload)
    print(response.json())

if __name__ == "__main__":
    url = 'https://www.iqiyi.com/v_19rzj6uadg.html'
    get_src(url)