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
    
    """ 利用python装饰器实现请求的重试 """
    @MYretry(client_exceptions.ServerDisconnectedError)
    async def request(self, url):
        async with self.semaphore:
            # try:
            print('getting', url)
            async with self.session.get(url) as response:
                await asyncio.sleep(1)
                return await response.read()
            # except client_exceptions.ServerDisconnectedError:
            #     print('ServerDisconnectedError occurred while scraping ',url)

    def save_pic(self, name, content):
        # 同步的写入文件
        name = os.path.join(self.save_path, name)
        with open(name, 'wb') as f:
            f.write(content)
            f.close()

    async def save_pic2(self, name, content):
        """ 未知是否异步 """
        name = os.path.join(self.save_path, name)
        async with aiofiles.open(name, mode='wb') as f:
            await f.write(content)

    def get_url_list(self, path):
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

    async def download_one(self, url, name):
        name = str(name).zfill(4)+'.jpg'
        content = await self.request(url)
        print('saved', name)
        if content:
            await self.save_pic2(name, content)

    async def main(self, url_list):
        self.session = aiohttp.ClientSession()
        # 添加任务一行写法
        tasks = [asyncio.ensure_future(self.download_one(
            url_list[i], i)) for i in range(len(url_list))]
        # tasks = []
        # for i in range(len(url_list)):
        #     tasks.append(asyncio.ensure_future(self.download_one(url_list[i],i)))
        await asyncio.gather(*tasks)
        await self.session.close()

    def run(self):
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)
        url_list = self.get_url_list('result.json')
        loop.run_until_complete(self.main(url_list))


if __name__ == "__main__":
    start_time = time.time()
    spider = Async_download()
    spider.run()
    print('cost', time.time()-start_time)
