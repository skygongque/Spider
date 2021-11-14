from typing import Dict
import requests
import time
import os
from util import downloadFILE
""" 
B站素材库平台视频抓取 https://cool.bilibili.com
免责申明：仅用于学习，请勿用于商业用途，否则产生的后果与本人无关
"""

class Bilibili:
    def __init__(self,download_path) -> None:
        """ 
            arg
                download_path 保存的路径
        """
        self.api = 'https://cool.bilibili.com/x/co-create/user/material/detail'
        self.list_api = 'https://cool.bilibili.com/x/co-create/material/list'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
        }
        self.download_path = download_path
        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path)
    
    def get_list(self,start_rank,cat_id) -> Dict:
        """ 获取列表页
            arg
                start_rank offset值用于翻页
                cat_id     类别 如180164 网络热梗
         """
        params = {
            'material_type': '19',
            'ps': '20',
            'start_rank': str(start_rank),
            'cat_id':str(cat_id),
            't': str(int(time.time()*1000))
        }
        response = requests.get(self.list_api,params=params,headers=self.headers)
        response.raise_for_status
        return response.json()

    def get_info(self,material_id) -> Dict:
        """ 
            获取详情页
                arg
                    material_id 素材id
                return
                    dict 包含素材title download_id等的字典
        """
        params = {
            'material_type':'19',
            'material_id':str(material_id),
            't':str(int(time.time()*1000))
        }
        response = requests.get(self.api,params=params,headers=self.headers)
        response.raise_for_status
        return response.json()

    def download(self,info):
        """ 根据info字典下载文件 """
        title = info['data']['title']
        download_url = info['data']['download_url']
        file_name =  title +'.' +download_url.split('.')[-1]
        file_name =  os.path.join(self.download_path,file_name)
        print(title,download_url)
        downloadFILE(download_url,file_name)
        

if __name__ == '__main__':
    b = Bilibili(download_path='网络热梗')
    # 根据 material_id 下载单个视频
    # b.download(b.get_info(940585))

    # 下载5页约100个
    for i in range(5):
        print('===========start_rank',i*20,'page',i+1,'=====================')
        # cat_id=120250 三连
        # cat_id=180164 网络热梗
        materials = b.get_list(start_rank=i*20,cat_id=180164)['data']['materials']
        for m in materials:
            print(m['title'],m['material_id'])
            info = b.get_info(m['material_id'])
            b.download(info)