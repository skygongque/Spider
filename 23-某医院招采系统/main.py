from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
import binascii
from Crypto.Cipher import AES  # pip install pycryptodome
import base64
import requests
import json
import re
""" 
参考文章 https://mp.weixin.qq.com/s/D4UJnOf56wfhEA35PXN7CA

"""
import subprocess
from functools import partial

subprocess.Popen = partial(subprocess.Popen, encoding="utf-8")
import  execjs

class AES_demo:
    def __init__(self,key) -> None:
        self.key = key

    def encrypt(self,content):
        k = self.key.encode("utf-8")
        pad = lambda s: s + (16 - len(s)%16) * chr(16 - len(s)%16) # 这里为Pkcs7填充
        content = pad(content).encode("utf-8")
        cipher = AES.new(k, AES.MODE_ECB) 
        cipher_text = cipher.encrypt(content)
        enc = base64.b64encode(cipher_text).decode("utf-8")
        return enc
    
    def decrypt(self,enc):
        enc = base64.b64decode(enc)
        cipher = AES.new(self.key.encode("utf-8"), AES.MODE_ECB)
        plain_text = cipher.decrypt(enc).decode('utf-8')
        return plain_text
    
class RSA_demo:
    def __init__(self,publicKey,privateKey) -> None:
        self.publicKey = publicKey
        self.privateKey = privateKey
        self.sentinel = get_random_bytes(16)

    def encrypt(self,content):
        publicKey_key = RSA.import_key(self.publicKey)
        cipher_rsa = PKCS1_v1_5.new(publicKey_key)
        cipher_text = cipher_rsa.encrypt(content.encode())
        enc =  base64.b64encode(cipher_text).decode("utf-8")
        return enc
    
    def decrypt(self,enc):
        # 私钥导入方式1
        private_key = RSA.import_key(self.privateKey)
        cipher_rsa = PKCS1_v1_5.new(private_key)
        # 密文
        plain_text = cipher_rsa.decrypt(binascii.a2b_base64(enc),sentinel=self.sentinel).decode()
        return plain_text

def process_epcos(e):
    with open('myencodeURL.js',encoding='utf-8') as f:
        js_code = f.read()
    ctx = execjs.compile(js_code)
    return ctx.call('my_encode',e)

def getBulletinDetailInfo(epcos,aesKey):
    url = f"https://zbcg.sznsyy.cn/sz/purchaser/public/getBulletinDetailInfo?epcos={epcos}"
    payload={}
    headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Referer': 'https://zbcg.sznsyy.cn/noticeDetail/3979/4/6',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'aesKey': aesKey,
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()


def download_file(epcos,aesKey):
    url = f"https://zbcg.sznsyy.cn/sz/file/download?epcos={epcos}"

    payload={}
    headers = {
    'Referer': 'https://zbcg.sznsyy.cn/noticeDetail/3979/4/6',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'aesKey': aesKey,
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.headers['Content-Disposition'].split(' ')[-1])
    save_file(epcos +'.pdf',response.content)


def save_file(path,content):
    with open(path,'ab') as f:
        f.write(content)



if __name__ == "__main__":
    private_key_str = """-----BEGIN RSA PRIVATE KEY-----
MIICdwIBADANBgkqhkiG9w0BAQEFAASCAmEwggJdAgEAAoGBALROqKeWuu+G6z6V7lesaAIC8FWWJ8qYRRy4HbbakJBH+OEWfD+0/MmMnZ28aMiV3qDy34SLfddDxvWJo/SR8iL8bjeqOEQxenu8Ogec+290w4F8IW6Ips/kZ5pnkg/TUn1GATOSV+RbB90okuykbBEbGKaNqGczJ/lI7RpfNvCpAgMBAAECgYA9RzJYaoizmRXgGlJ7Z3Odo2QMolB5sRBj90rZ9yQEdQFndh3aBOeYk/qJPhwad5zG9GP0hvfIrhczIYkgOG2i1ZvBAFBP7IZiGJz5PxS9QOFPg926sI6Mv3nBIS0+U88IyzPL/fQWNvhc3b9Y95kYp4p0Wk4zzNe9HNNUMQHdUQJBAOwA6EoVSlxlpNivoAGrMynLlnHmZ7fEpXXQINUbhpX8+I3fazoWcRaYpfLmVKa82DJXHUe8URFX3oir3kAocVUCQQDDlahWFmYmtNYqLitJdIdltTcmQtAgHlfshdYnq6Gg8jSjwh40sXF8MgZfG03+sfdmKbSG3e+7Ihb/X5P/odIFAkEAlz3Rn0BbojDlXpPWN5uOMzesFxwv1Z3o50JU+B0mt9IhO1I1dklRecijeLFRCHW3GzOmqQUu8q1cCDwUNwtz7QJBAJ3BT8coR/q+b+QT20xjVnaeBT6yM2dEskyP4x2aXUMROY5Am9aKrWuseeEqh+2ApHld+EO0LZJ2O7B96kUNw/UCQHhXTTBHc2HkyU84U2+OAB2hJtJBmj+eGl0iqNfOq3JyiIemC/bV74sASLa+NN9CJRotBh9jzmzNpwEi24Y8KHE=
-----END RSA PRIVATE KEY-----"""
    publicKey = """-----BEGIN RSA PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCC3Lb0O4zgEakDfJ4XJO5zadXep9bQeWyJ6pa0e328PYQYZgLNP7eVrAP7mVZgG+8D4MicIcStTQnBxF8AEyJKrh/M/3WSSK2zDvrZn1paWf4SA8zFIn5cuYlcUH+WuxghQn3kKRUW2qtBY9eaGF5qntascctNgQTHmW3eqQzDBQIDAQAB
-----END RSA PUBLIC KEY-----"""
    content = 'QewVpuECaB5VW7oXGgVFFsm9YXm8sLf5c7ZnddMJE0rLldXLf8T6pMyEh5HjZsiqekXpGEl6cu82BlC1W3mOWEhmNpKPSZGbzTjXuPkqetOcdvUK951sUGi9XWuyb4PbPBmWK89eE6oxaQB56+bAplVzdgQ5FrD5XiCua++EPYw='
    r = RSA_demo(privateKey=private_key_str,publicKey=publicKey)
    aeskey = "N3MVSgK47x499qts"
    enc_aeskey = r.encrypt(aeskey)
    print(enc_aeskey)
    # de_asekey = r.decrypt(content)
    # print(de_asekey)
    # params = "noticeType=4&middleId=3979"
    params = "noticeType=4&middleId=4054"
    a = AES_demo(key=aeskey)
    epcos_temp =a.encrypt(params)
    # epcos = base64.encode(epcos_temp.encode()).replace('=','+')
    print(epcos_temp)
    print(enc_aeskey)
    # epcos = process_epcos(epcos_temp)
    # print(epcos)
    detailInfo = getBulletinDetailInfo(epcos=process_epcos(epcos_temp),aesKey=enc_aeskey)
    print(detailInfo)
    de_aesKey = r.decrypt(detailInfo['aesKey'])
    d_aes = AES_demo(key=de_aesKey)
    plaindetailInfo  =  d_aes.decrypt(detailInfo['content']) 
    # "announcementKey":"ae3577031d8d469d86d0c05768449232"
    find_announcementKey = re.search('"announcementKey":"(.*?)"',plaindetailInfo)
    if find_announcementKey:
        download_file(epcos=process_epcos(a.encrypt('fileKey='+find_announcementKey.group(1))),aesKey=enc_aeskey)
   


