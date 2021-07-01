'''
Function:
    微信公众号文章爬取
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import os
import time
import json
import pdfkit
import random
import requests
import warnings
warnings.filterwarnings('ignore')


'''微信公众号文章爬取类'''
class articlesSpider(object):
    def __init__(self, cfg, **kwargs):
        self.cfg = cfg
        self.session = requests.Session()
        self.__initialize()
    '''外部调用'''
    def run(self):
        self.__getArticleLinks()
        # self.__downloadArticles()
    '''获得所有文章的链接'''
    def __getArticleLinks(self):
        print('[INFO]: 正在获取目标公众号的所有文章链接...')
        fp = open('links_tmp.json', 'w', encoding='utf-8')
        article_infos = {}
        params = {
                    'action': 'getmsg',
                    '__biz': self.cfg.biz,
                    'f': 'json',
                    'offset': '0',
                    'count': '10',
                    'is_ok': '1',
                    'scene': '123',
                    'uin': '777',
                    'key': '777',
                    'pass_ticket': self.cfg.pass_ticket,
                    'wxtoken': '',
                    'appmsg_token': self.cfg.appmsg_token,
                    'x5': '0'
                }
        while True:
            res = self.session.get(self.profile_url, params=params, verify=False)
            print(self.profile_url)
            # print(res.text)
            res_json = res.json()
            can_msg_continue = res_json.get('can_msg_continue', '')
            next_offset = res_json.get('next_offset', 10)
            general_msg_list = json.loads(res_json.get('general_msg_list', '{}'))
            params.update({'offset': next_offset})
            for item in general_msg_list['list']:
                app_msg_ext_info = item.get('app_msg_ext_info', {})
                if not app_msg_ext_info: continue
                title = app_msg_ext_info.get('title', '')
                content_url = app_msg_ext_info.get('content_url', '')
                if title and content_url:
                    article_infos[title] = content_url
                if app_msg_ext_info.get('is_multi', '') == 1:
                    for article in app_msg_ext_info.get('multi_app_msg_item_list', []):
                        title = article.get('title', '')
                        content_url = article.get('content_url', '')
                        if title and content_url:
                            article_infos[title] = content_url
            if can_msg_continue != 1: break
            else: time.sleep(1+random.random())
        json.dump(article_infos, fp)
        fp.close()
        print('[INFO]: 已成功获取目标公众号的所有文章链接, 数量为%s...' % len(list(article_infos.keys())))
    '''下载所有文章'''
    def __downloadArticles(self):
        print('[INFO]: 开始爬取目标公众号的所有文章内容...')
        if not os.path.exists(self.savedir):
            os.mkdir(self.savedir)
        fp = open('links_tmp.json', 'r', encoding='utf-8')
        article_infos = json.load(fp)
        for key, value in article_infos.items():
            print('[INFO]: 正在抓取文章 ——> %s' % key)
            key = key.replace('//', '').replace('/', '').replace(':', '').replace('：', '') /
                     .replace('*', '').replace('?', '').replace('？', '').replace('“', '')  /
                     .replace('"', '').replace('<', '').replace('>', '').replace('|', '_')
            pdfkit.from_url(value, os.path.join(self.savedir, key+'.pdf'), configuration=pdfkit.configuration(wkhtmltopdf=self.cfg.wkhtmltopdf_path))
        print('[INFO]: 已成功爬取目标公众号的所有文章内容...')
    '''类初始化'''
    def __initialize(self):
        self.headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1295.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat'
                    }
        self.cookies = {
                        'wxuin': '913366226',
                        'devicetype': 'iPhoneiOS13.3.1',
                        'version': '17000c27',
                        'lang': 'zh_CN',
                        'pass_ticket': self.cfg.pass_ticket,
                        # 'wap_sid2': 'CNK5w7MDElxvQU1fdWNuU05qNV9lb2t3cEkzNk12ZHBsNmdXX3FETlplNUVTNzVfRmwyUUtKZzN4QkxJRUZIYkMtMkZ1SDU5S0FWQmtSNk9mTTQ1Q1NDOXpUYnJQaDhFQUFBfjDX5LD0BTgNQJVO'
                        'wap_sid2': self.cfg.wap_sid2
                    }
        self.profile_url = 'https://mp.weixin.qq.com/mp/profile_ext'
        self.savedir = 'articles'
        self.session.headers.update(self.headers)
        self.session.cookies.update(self.cookies)


'''run'''
if __name__ == '__main__':
    import cfg
    spider = articlesSpider(cfg)
    spider.run()