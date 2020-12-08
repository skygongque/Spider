""" 蜻蜓FM有声书批量下载支持账号登录 """
import requests
import re
import hmac
import time
from tqdm import tqdm
from bs4 import BeautifulSoup
import os
import json
import sys
import urllib3
urllib3.disable_warnings()

class QingTing():
    def __init__(self,user_id,password,bookurl,ifLogin):
        self.ifLogin = ifLogin
        self.user_id = user_id
        self.password = password
        self.session = requests.session()    
        self.session.headers.update({'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'})
        self.login_url = "https://u2.qingting.fm/u2/api/v4/user/login"
        self.bookurl = bookurl
        self.bookid = self.bookurl.split('/')[-1]
        self.qingtinghost = 'https://audio.qingting.fm'
        self.save_path = ''
        self.bookname = ''

    def login(self,user_id,password):
        """ return qingting_id  access_token"""
        data = {
            'account_type': '5',
            'device_id': 'web',
            'user_id': user_id,
            'password': password
        }
        response = self.session.post(self.login_url,data=data,verify=False)
        if response.status_code==200:
            temp = response.json()
            errorno = temp['errorno']
            errormsg = temp['errormsg']
            if errorno == 0:
                print('login successful!','登录成功！')
                data = temp['data']
                return data['qingting_id'],data['access_token']
                # self.qingting_id = data['qingting_id']
                # self.access_token = data['access_token']
            
            else:
                print('Login failed','登录失败')
                print(errormsg)
                # config中配置了登录但登录失败等待十秒后退出
                time.sleep(10)
                sys.exit(0)
    
    def __get_version(self):
        response =  self.session.get(url=self.bookurl,verify=False)
        if response.status_code==200:
            soup = BeautifulSoup(response.text,'lxml')
            temp_bookname = soup.select('div.album-info-root > div.top > div.info.right > h1')[0].string
            # 替换文件名中的非法字符
            replaced_pattern = '[\\\/:\*\?\"<>|]'
            self.bookname = re.sub(replaced_pattern,' ',temp_bookname,flags=re.M +re.S)
            if not os.path.exists(self.bookname):
                os.makedirs(self.bookname)
            matched = re.search('\"version\":\"(\w+)"',response.text,re.S)
            if matched:
                version = matched.group(1)
                return version
                # return version
    
    def __get_total_page(self,bookid,version):
        page = 1
        info_api = f'https://i.qingting.fm/capi/channel/{bookid}/programs/{version}?curpage={str(page)}&pagesize=30&order=asc'
        response =  self.session.get(info_api,verify=False)
        if response.status_code==200:
            temp =  response.json()
            total = temp['data']['total']
            total_page = int(int(total)/30)+1
            return total,total_page
    


    def get_book_info(self,bookid,version):
        total,total_page = self.__get_total_page(bookid,version)
        print(self.bookname,'共{}集'.format(total))
        for page in range(1,total_page+1):
            info_api = f'https://i.qingting.fm/capi/channel/{bookid}/programs/{version}?curpage={str(page)}&pagesize=30&order=asc'
            response =  self.session.get(info_api,verify=False)
            programs = response.json()['data']['programs']
            for program in programs:
                # print(program['id'],program['title'])
                yield program

    def get_src(self,id,access_token,qingting_id):
        bookid = self.bookid
        timestamp = str(round(time.time()*1000))
        if access_token and qingting_id:
            data = f"/audiostream/redirect/{bookid}/{id}?access_token={access_token}&device_id=MOBILESITE&qingting_id={qingting_id}&t={timestamp}"
        else:
            data = f"/audiostream/redirect/{bookid}/{id}?access_token=&device_id=MOBILESITE&qingting_id=&t={timestamp}"
        message = data.encode('utf-8')
        key = "fpMn12&38f_2e".encode('utf-8')
        sign = hmac.new(key, message, digestmod='MD5').hexdigest()
        whole_url = self.qingtinghost+data+"&sign="+sign
        return whole_url
    
    def downloadFILE(self,url,name):
        resp = self.session.get(url=url,stream=True,verify=False)
        if resp.headers['Content-Type'] =='audio/mpeg':
            content_size = int(int(resp.headers['Content-Length'])/1024)
            with open(name, "wb") as f:
                print("Pkg total size is:",content_size,'k,start...')
                for data in tqdm(iterable=resp.iter_content(1024),total=content_size,unit='k',desc=name):
                    f.write(data)
                print(name , "download finished!")
        else:
            errorno = resp.json()['errorno']
            errormsg = resp.json()['errormsg']
            print('没有权限下载,请登录已购此音频的账号。')
            print('errorno:',errorno,errormsg)

        
        

    def run(self):
        qingting_id = None
        access_token = None
        if self.ifLogin:
            qingting_id,access_token = self.login(self.user_id,self.password)
        version = self.__get_version()
        programs =  self.get_book_info(self.bookid,version)
        for count,program in enumerate(programs):
            try:
                title = str(count).zfill(4)+' '+program['title']+'.m4a'
                if not self.bookname =='':
                    title = os.path.join(self.bookname,title)
                whole_url =  self.get_src(program['id'],access_token,qingting_id)
                self.downloadFILE(whole_url,title)
            except Exception as e:
                print(e)
                with open('log.txt','a',encoding='utf-8') as f:
                    f.write(str(count)+str(e)+'\n')

def get_config_info():
    with open('config.json','r',encoding='utf-8') as f:
        config = json.loads(f.read())
        return config

if __name__ == "__main__":
    # pyinstaller -F -i ico.ico QingTingFM.py
    config = get_config_info()
    if config["ifLogin"]:
        bookurl = input('请输入要下载音频的主页链接:(如https://www.qingting.fm/channels/257790)')
        isvalid = re.search('https://www.qingting.fm/channels/\d+',bookurl)
        if isvalid:
            q  = QingTing(config["user_id"],config["password"],bookurl,1)
            q.run()
        else:
            print("输入的主页格式错误")
    else:
        # 不登录
        bookurl = input('请输入要下载音频的主页链接:(如https://www.qingting.fm/channels/257790)')
        isvalid = re.search('https://www.qingting.fm/channels/\d+',bookurl)
        if isvalid:
            q  = QingTing(config["user_id"],config["password"],bookurl,0)
            q.run()
        else:
            print("输入的主页格式错误")