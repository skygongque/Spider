from Crypto.Cipher import AES
import base64
import hashlib
import json
import requests
# import pymongo
import time
from requests import exceptions
import pandas as pd


# 连接数据库
# client = pymongo.MongoClient()
# db = client['Netease_2']
 
# def save_to_mongo(data):
#     """ 存入mongodb数据库 """
#     # 按commentId更新
#     if db['comments'].update({'commentId': data['commentId']}, {'$set': data}, True):
#         print('Saved to Mongo', data["nickname"],data["content"])
#     else:
#         print('Saved to Mongo Failed', data['commentId'])
 

def save_csv(data_list):
    df = pd.DataFrame(data_list)
    df.to_csv('result.csv')

def save_excel(data_list):
    df = pd.DataFrame(data_list)
    df.to_excel('result4.xlsx')

class Netease:
    def __init__(self):
        self.key1 = b'0CoJUm6Qyw8W8jud'
        self.key2 = b"ihPb70NS86eAsg9M"
        self.encSecKey = "3bc924d00a13c5c27664d436967a26bb13cca16e576f53ed642298406b26ffd3340805b2c563969cb6462d2c93c41c50e6684e1dce8fb63f6e3fd5c95e8e8375f727ebe195530c4989bcc897e3eec4107850ee126b6f95a184432d0eaf6cba1c6e0e37e86d83bf7e3f670f7790d3d8ded5f7391f746554311f31cb9b430fff10"
        self.login_url_phone = 'http://music.163.com/weapi/login/cellphone'
        self.base_comments_API = "https://music.163.com/weapi/v1/resource/comments/R_SO_4_"
        self.csrf_token = ''
        self.headers = {
            'Accept':'*/*',
            'Accept-Language':'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
            'Connection':'keep-alive',
            'Content-Type':'application/x-www-form-urlencoded',
            'Referer':'http://music.163.com',
            'Host':'music.163.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.all_data_list = []
 
    def _encrypt(self,data):
        """ 两次aes加密 """
        data_string = json.dumps(data)
        temp = self._ase_encrypt(self.key1,data_string)
        return self._ase_encrypt(self.key2,temp),self.encSecKey
 
 
    def _ase_encrypt(self,key,content):
        pad = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
        my_ase = AES.new(key=key,mode=AES.MODE_CBC,IV=b'0102030405060708')
        return base64.b64encode(my_ase.encrypt(pad(content).encode())).decode()
     
    def login(self,phone,password):
        """ 登录，此处仅支持手机号，邮箱另一个接口 """
        md5 = hashlib.md5()
        md5.update(password.encode('utf-8'))
        password = md5.hexdigest()
        data = {
            'phone':phone,
            'password': password,
            'rememberLogin': True
                    }
        params,encSecKey = self._encrypt(data)
        post_data = {
            'params': params,
            'encSecKey': encSecKey,
        }
        response =  self.session.post(self.login_url_phone,data=post_data)
        if response.status_code ==200:
            res_json = response.json()
            # 登录成功
            if res_json['code'] ==200:
                print('login successfully')
                ckjar = self.session.cookies
                ck_dict = requests.utils.dict_from_cookiejar(ckjar)
                self.csrf_token = ck_dict['__csrf']
                # print(self.csrf_token)
 
            elif(res_json['code'] == 400) or (res_json['code'] == 502):
                print('fail to login, username or password error')
            else:
                print(res_json.get('msg'))
             
 
 
 
    def get_one_page(self,song_id,page):
        """ 抓取一页 """
        print('current page:',page)
        data = {"rid":f"R_SO_4_{str(song_id)}","offset":f"{str((page-1)*20)}","total":"false","limit":"20","csrf_token":f"{self.csrf_token}"}
        params,encSecKey = self._encrypt(data)
        post_data = {
            'params': params,
            'encSecKey': encSecKey,
        }
        try:
            response = self.session.post(url=self.base_comments_API+str(song_id),data=post_data)
            if response.status_code ==200:
                # print(response.json())
                return response.json()
            else:
                print(response.status_code)
        except exceptions.ProxyError:
            time.sleep(3)
            print('try again...')
            return self.get_one_page(song_id,page)
     
    def get_last_50_comments(self,song_id,total):
        """ 抓取最后50页 """
        total_page = int(int(total)/20)+1
        for page in range(total_page-50,total_page+1):
            res_json = self.get_one_page(song_id,page)
            more = res_json['more']
            comments = res_json['comments']
            for comment in comments:
                data = self.parse_each_comment(comment)
                data['song_id'] = song_id
                self.all_data_list.append(data)
            time.sleep(1)
            if not more:
                break
 
    def parse_each_comment(self,comment):
        nickname = comment["user"]["nickname"]
        userId = comment["user"]["userId"]
        content = comment["content"]
        time = comment["time"]
        likedCount = comment["likedCount"]
        commentId = comment["commentId"]
        return {
            "userId":userId,
            "nickname":nickname,
            "content":content,
            "time":time,
            "likedCount":likedCount,
            "commentId":commentId
        }
 
    def run(self):
        # 登录没用
        # self.login('','')
         
        # 抓取指定song_id下的最多约2000条评论
        song_id = 1455658167
        for page in range(1,101):
            print('page',page)
            res_json = self.get_one_page(song_id,page)
            more = res_json['more']
            comments = res_json['comments']
            for comment in comments:
                data = self.parse_each_comment(comment)
                data['song_id'] = song_id
                self.all_data_list.append(data)
            time.sleep(1)
            if not more:
                # if page <100:
                #     """需要抓取最后50页 """
                #     total = self.get_one_page(song_id,1)['total']
                #     self.get_last_50_comments(song_id,total)
                break
        save_excel(self.all_data_list)
 
if __name__ == "__main__":
    t = Netease()
    t.run()
    """ MongoDB的query """
    # {"userId":123}    # 精确查找userId为123的评论
    # {"content":{"$regex":"123"}}   #模糊查找评论内容包含123字符的评论