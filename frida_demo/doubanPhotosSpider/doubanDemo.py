import base64
import hmac
import hashlib
import urllib.parse
import requests
import time


def encrypt(text):
    digest = hmac.new(b'bf7dddc7c9cfe6f7', text.encode(),
                      hashlib.sha1).digest()
    return base64.b64encode(digest).decode("utf-8")


def get_sig(params):
    text = r'GET&%2Fapi%2Fv2%2Felessar%2Fsubject%2F{}%2Fphotos&{}'.format(
        params['num'], params['ts'])
    return urllib.parse.quote(encrypt(text))


def requestData(info,start):
    # url = "https://frodo.douban.com/api/v2/elessar/subject/27503300/photos?os_rom=android&apikey=0dad551ec0f84ed02907ff5c42e8ec70&channel=Yingyongbao_Market&udid=a89cdbc09b19168fa564b64bfc4a5f3bee201801&_sig=bn02VM%2b8JgXMymgBjcLL%2fu8Y%2fAE%3d&_ts=1603605177"
    url = "https://frodo.douban.com/api/v2/elessar/subject/{}/photos?start={}&count=100&os_rom=android&apikey=0dad551ec0f84ed02907ff5c42e8ec70&channel=Yingyongbao_Market&udid=a89cdbc09b19168fa564b64bfc4a5f3bee201801&_sig={}&_ts={}".format(info['num'],start,get_sig(info),info['ts'])
    # params = {
    #     'os_rom': 'android',
    #     'apikey': '0dad551ec0f84ed02907ff5c42e8ec70',
    #     'channel': 'Yingyongbao_Market',
    #     'udid': 'a89cdbc09b19168fa564b64bfc4a5f3bee201801',
    #     '_sig': 'bn02VM%2b8JgXMymgBjcLL%2fu8Y%2fAE%3d',
    #     '_ts': '1603605177'
    # }
    headers = {
        'User-Agent': 'api-client/1 com.douban.frodo/6.45.0(197) Android/22 product/PCRT00 vendor/OPPO model/PCRT00  rom/android  network/wifi  platform/AndroidPad nd/1',
        'Host': 'frodo.douban.com',
        'Cookie': 'bid=AraQ8v07k-M'
    }
    response = requests.get(url=url, headers=headers)
    print(response.json())
    return response.json()


def parse(res_json):
    photos = res_json['photos']
    if len(photos) > 0:
        images = []
        for photo in photos:
            image = photo['image']['large']['url']
            images.append(image)
        return images
    else:
        return -1
    

if __name__ == "__main__":
    info = {
        'num': '27503300',
        'ts': str(int(time.time()))
    }
    i = 0
    while (True):
        print('start:',i*50)
        res = requestData(info,str(i*50))
        images = parse(res)
        print(images)
        if images == -1:
            break
        else:
            i += 1
