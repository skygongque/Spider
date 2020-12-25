import requests
import warnings
import json
import time
import random

warnings.filterwarnings('ignore')


class WxArtcile:
    def __init__(self, config):
        self.profile_url = "https://mp.weixin.qq.com/mp/profile_ext"
        self.config = config
        self.headers = {
            'Host': 'mp.weixin.qq.com',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1301.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat',
            'x-requested-with': 'XMLHttpRequest',
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.5;q=0.4'
        }

    def __getLink(self,offset):
        params = {
            'action': 'getmsg',
            '__biz': config['__biz'],
            'f': 'json',
            'offset': offset,
            'count': 10,
            'is_ok': 1,
            'scene': '',
            'uin': config['uin'],
            'key': config['key'],
            'pass_ticket': config['pass_ticket'],
            'wxtoken': '',
            'appmsg_token': config['appmsg_token'],
        }
        response = requests.get(self.profile_url, params=params, headers=self.headers, verify=False)
        return response.json()




    def run(self):
        offset = 0
        # print(res_json)
        article_infos = {}
        while True:
            print('[正在爬取文章链接],当前offset=>',offset)
            res_json = self.__getLink(offset)
            general_msg_list = res_json["general_msg_list"]
            next_offset = res_json["next_offset"]
            can_msg_continue = res_json.get('can_msg_continue', '')
            next_offset = res_json.get('next_offset', 10)
            general_msg_list = json.loads(res_json.get('general_msg_list', '{}'))
            offset = next_offset
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
        print('[INFO]: 已成功获取目标公众号的所有文章链接, 数量为%s...' % len(list(article_infos.keys())))
        with open('articleLinks.json','w',encoding='utf-8') as f:
            f.write(json.dumps(article_infos,ensure_ascii=False))
            f.close

if __name__ == "__main__":
    config = {
        '__biz': 'MzAwNTY1OTg0MQ==',
        'uin': '',
        'key': '',
        'pass_ticket': '',
        'appmsg_token': ''
    }
    w = WxArtcile(config)
    w.run()


