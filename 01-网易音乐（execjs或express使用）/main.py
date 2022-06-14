import requests
# 解决execjs经典的 gbk报错问题
import subprocess
from functools import partial

subprocess.Popen = partial(subprocess.Popen, encoding="utf-8")
import execjs



class Netease:
    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
        }
        self.nodejs_url = 'http://127.0.0.1:3000/encrypt'
        self.post_url = 'https://music.163.com/weapi/song/enhance/player/url/v1'

    def get_params(self,ids):
        """ execjs 执行js代码返回加密后的params 即'encText', 'encSecKey'"""
        with open('163.js','r',encoding='utf-8') as f:
            jstext = f.read()
            ctx = execjs.compile(jstext)
            params = ctx.call('get_params',ids)
            return params
    
    def get_from_node_server(self,ids):
        """ 从运行在本地的 HTTP API 获取加密后的params 通过node.js的express框架实现 """
        data = {
            'ids':ids
        }
        response = requests.post(self.nodejs_url,data=data)
        if response.status_code==200:
            return response.json()

    def get_src(self,params):
        data = {
            'params':params['encText'],
            'encSecKey':params['encSecKey']
        }
        response = requests.post(self.post_url,data=data,headers=self.headers)
        if response.status_code ==200:
            return response.json()['data']


    def run(self):
        # 传入一个或多个歌曲的id 打印歌曲的真实地址，传入多个id时返回的歌曲顺序可能打乱
        ids = [1357850926,492144016]
        # 用excejs 加密
        params =  self.get_params(str(ids))
        # 请求本地API 加密 需要先开启服务 node server.js
        # params = self.get_from_node_server(str(ids))
        srcs =  self.get_src(params)
        for src in srcs:
            print('id:',src['id'],'url:',src['url'])


if __name__ == "__main__":
    m = Netease()
    m.run()

