import aiohttp
import asyncio
import aiofiles
import json
import os
import time
from aiohttp import client_exceptions
from pictureDownloader.asyncFunctionRetry import *

loop = asyncio.get_event_loop()


class AsyncDownloader:
    def __init__(self,save_path):
        super().__init__()
        self.CONCURRENCY = 5
        self.session = None
        self.semaphore = asyncio.Semaphore(self.CONCURRENCY)
        self.save_path = save_path
    
    """ 利用python装饰器实现请求的重试 """
    @asyncFunctionRetry(client_exceptions.ServerDisconnectedError,client_exceptions.ClientPayloadError)
    async def request(self, url):
        async with self.semaphore:
            # print('getting', url)
            # 添加ssl=False 防止SSLCertVerificationError 
            async with self.session.get(url,ssl=False) as response:
                await asyncio.sleep(1)
                return await response.read()

    async def save_pic(self, name, content):
        """ 未知是否异步 """
        name = os.path.join(self.save_path, name)
        async with aiofiles.open(name, mode='wb') as f:
            await f.write(content)

    async def download_one(self, url, name):
        # name = str(name).zfill(4)+'.jpg'
        name = str(name).zfill(4)+'.png'
        content = await self.request(url)
        print('saved', name)
        if content:
            await self.save_pic(name, content)

    async def asyncTasks(self, url_list):
        self.session = aiohttp.ClientSession()
        # 添加任务一行写法
        tasks = [asyncio.ensure_future(self.download_one(
            url_list[i], i)) for i in range(len(url_list))]
        # tasks = []
        # for i in range(len(url_list)):
        #     tasks.append(asyncio.ensure_future(self.download_one(url_list[i],i)))
        await asyncio.gather(*tasks)
        await self.session.close()


def get_url_list(path):
    url_list = []
    with open(path, 'r', encoding='utf-8') as f:
        res_json = json.loads(f.read())
        for card in res_json:
            if card['card_type'] == 47:
                for pic in card['pics']:
                    if pic['pic_big'][-4:] == '.gif':
                        continue
                    url_list.append(pic['pic_big'])
        return url_list      



if __name__ == "__main__":
    start_time = time.time()
    save_path = 'result'
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    ad = AsyncDownloader(save_path)
    url_list = get_url_list('result.json')
    loop.run_until_complete(ad.asyncTasks(url_list))
    print('cost', time.time()-start_time)
