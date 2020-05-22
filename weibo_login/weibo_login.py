""" 
参考https://github.com/CharlesPikachu/DecryptLogin/blob/master/DecryptLogin/platforms/weibo.py
"""
import requests
import base64
import time
import random
# rsa用的是PKCS1_v1_5填充
import rsa
import re
import json
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import PKCS1_v1_5
from binascii import b2a_hex
from PIL import Image
import warnings
# 过滤警告信息
warnings.filterwarnings('ignore')

class weibo:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        }
        self.prelogin_url = 'https://login.sina.com.cn/sso/prelogin.php'
        self.ssologin_url = 'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)'
        self.pin_url = 'https://login.sina.com.cn/cgi/pin.php'
        self.login_url = 'https://passport.weibo.com/wbsso/login?'
        self.home_url = 'https://weibo.com/u/%s/home'

    def get_prelogin_info(self,username,password):
        """ 请求prelogin_url得到RSA加密的参数 """
        su = base64.b64encode(username.encode())
        su = str(su,'utf-8')
        params = {
            'entry': 'account',
            # 'callback': 'sinaSSOController.preloginCallBack',
            'su': su,
            'rsakt': 'mod',
            'client': 'ssologin.js(v1.4.15)',
            '_': str(int(time.time()*1000))
        }
        # verify=False 不加也可以返回数据
        res = self.session.get(self.prelogin_url, params=params, verify=False)
        return res.json()

    def get_pin(self):
        """ 保存验证码图片 """
        r = int(random.random()*100000000)
        params = {
			'r': str(r),
			's': '0',
		}
        response = self.session.get(self.pin_url,params=params)
        if response.status_code ==200:
            with open('pin_img.png','wb') as f:
                f.write(response.content)
                f.close()
                print('had saved Captcha.')
            # Image好像会调用默认的图片查看器打开图片
            I = Image.open('pin_img.png')
            I.show()
            Captcha_value = input('enter the Captcha value:')
            return Captcha_value

    def post_login_data(self,username,password,Captcha_value=None): 
        """ post请求登录 """  
        p = self.get_prelogin_info(username,password)
        
        # 用不同的库实现RSA加密 都可行
        """ RSA库实现 """
        # publickey = rsa.PublicKey(int(p['pubkey'], 16), int('10001', 16))
        # sp = rsa.encrypt((str(p['servertime'])+'\t'+p['nonce']+'\n'+password).encode(), publickey)
        
        """ 用pycryptodome库实现 """
        rsa_public_key = RSA.construct((int(p['pubkey'],16),int('10001',16)))
        cipher_rsa = PKCS1_v1_5.new(rsa_public_key)
        sp2 = cipher_rsa.encrypt((str(p['servertime'])+'\t'+p['nonce']+'\n'+password).encode())
        # 返回的二进制数据的十六进制表示
        sp = b2a_hex(sp2)
        data_post = {
            'entry': 'account',
            'gateway': '1',
            'from': '',
            'savestate': '30',
            'useticket': '0',
            'pagerefer': '',
            'vsnf': '1',
            'su': base64.b64encode(username.encode()),
            'service': 'account',
            'servertime': str(int(p['servertime'])+random.randint(1, 20)),
            'nonce':p['nonce'],
            'pwencode': 'rsa2',
            'rsakv': p['rsakv'],
            'sp': sp,
            'sr': '1366*768',
            'encoding': 'UTF-8',
            'cdult': '3',
            'domain': 'sina.com.cn',
            'prelt': '95',
            'returntype': 'TEXT',
        }
        if Captcha_value:
            data_post['door'] = Captcha_value
        res = self.session.post(self.ssologin_url, data=data_post,allow_redirects=False, verify=False)
        if res.status_code==200:
            return res.json()
    
    def check_at_login_url(self,res,username):
        ticket, ssosavestate = re.findall(r'ticket=(.*?)&ssosavestate=(.*?)"', res)[0]
        # 请求login_url
        params = {
                    'ticket': ticket,
                    'ssosavestate': str(ssosavestate),
                    'callback': 'sinaSSOController.doCrossDomainCallBack',
                    'scriptId': 'ssoscript0',
                    'client': 'ssologin.js(v1.4.19)',
                    '_': str(int(time.time() * 1000))
                }
        params = '&'.join(['%s=%s' % (key, value) for key, value in params.items()])
        res = self.session.get(self.login_url+params, verify=False)
        uid = re.findall(r'"uniqueid":"(.*?)"', res.text)[0]
        res = self.session.get(self.home_url % uid, verify=False)
        if '我的首页' in res.text:
            print('[INFO]: Account -> %s, login successfully...' % username)
            infos_return = {'username': username}
            return infos_return, self.session

    
    def login(self,username,password):
        res = self.post_login_data(username,password)
        while True:
            if res['retcode']=='0':
                infos_return,login_session = self.check_at_login_url(json.dumps(res),username)
                if login_session:
                    return login_session
                break
            elif res['retcode']=='101':
                # 用户名或密码不正确
                print(res['reason'])
                break
            elif res['retcode']=='4049':
                # 需要验证码
                print(res['reason'])
                res = self.post_login_data(username,password,self.get_pin())
            elif res['retcode']=='2070':
                # 验证码错误
                print(res['reason'])
                res = self.post_login_data(username,password,self.get_pin())
            else:
                print(res)
                break
        


if __name__ == "__main__":
    t = weibo()
    # t.login('用户名','密码')
    login_session = t.login('','')
    # print(login_session.cookies)
    