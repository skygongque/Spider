import base64
import hmac
import hashlib
import urllib.parse
import requests
import time
import aiohttp
import asyncio
import aiofiles
import json
import os
import time
from aiohttp import client_exceptions
from MYretry import *
 
loop = asyncio.get_event_loop()
 
class Async_download:
    def __init__(self):
        super().__init__()
        self.CONCURRENCY = 5
        self.session = None
        self.semaphore = asyncio.Semaphore(self.CONCURRENCY)
        self.save_path = 'result'
 
    @MYretry(client_exceptions.ServerDisconnectedError)
    async def request(self, url):
        async with self.semaphore:
            # try:
            print('getting',url)
            async with self.session.get(url) as response:
                await asyncio.sleep(1)
                return await response.read()
            # except client_exceptions.ServerDisconnectedError:
            #     print('ServerDisconnectedError occurred while scraping ',url)
             
    def save_pic(self,name,content):
        # 同步的写入文件
        name = os.path.join(self.save_path,name)
        with open(name,'wb') as f:
            f.write(content)
            f.close()
 
    async def save_pic2(self,name,content):
        name = os.path.join(self.save_path,name)
        async with aiofiles.open(name, mode='wb') as f:
            await f.write(content)
  
     
    async def download_one(self,url,name):
        # name = str(name).zfill(4)+'.jpg'
        content = await self.request(url)
        print('saved',name)
        if content:
            await self.save_pic2(name,content)  
 
    async def main(self,url_list,page):
        # connector=aiohttp.TCPConnector(limit=64,verify_ssl=False)
        self.session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=64,verify_ssl=False))
        # 添加任务一行写法
        tasks = [asyncio.ensure_future(self.download_one(url_list[i],str(page).zfill(2)+"-"+str(i).zfill(3)+'.jpg')) for i in range(len(url_list))]
        # tasks = []
        # for i in range(len(url_list)):
        #     tasks.append(asyncio.ensure_future(self.download_one(url_list[i],i)))
        await asyncio.gather(*tasks)
        await self.session.close()
 
    def run(self,url_list,page):
        loop.run_until_complete(self.main(url_list,page))


# 豆瓣相关
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
    start_time = time.time()
    spider = Async_download()
    info = {
        'num': '27503300',
        'ts': str(int(time.time()))
    }
    i = 0
    images = None
    while (True):
        print('start:',i*50)
        if images != -1:
            res = requestData(info,str(i*50))
            images = parse(res)
            spider.run(url_list=images,page=i+1)
            i += 1
        else:
            break
    print('cost',time.time()-start_time)



