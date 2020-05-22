import requests
import json
# 'Cookie': '换成自己登录后的cookie'

def get_next_page(page):
    url = f'https://m.weibo.cn/api/container/getSecond?containerid=1078033669102477_-_photoall&page={str(page)}&count=24&title=%E5%9B%BE%E7%89%87%E5%A2%99&luicode=10000011&lfid=1078033669102477&type=uid&value=3669102477'
    headers = {
        # 'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': '*/*',
        #   'Referer': 'https://weibo.com/p/1004063669102477/photos?from=page_100406&mod=TAB',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en;q=0.7',
        'Cookie': '换成自己登录后的cookie',
        
    }
    response = requests.request("GET", url, headers=headers)
    return response.json()


def parse(res_json):
    if 'data' in res_json.keys():
        cards = res_json['data']['cards']
        if len(cards) == 0:
            return False
        else:
            return cards

def save_list(result):
    """ 保存结果 """
    with open('result.json','a',encoding='utf-8') as f:
        f.write(json.dumps(result,ensure_ascii=False))
        f.close()


def main():
    all_cards = []
    page = 0
    while True:
        page += 1
        cards = parse(get_next_page(page))
        # print(cards)
        print('page',page)
        if cards:
            # all_cards.append(cards)
            all_cards +=cards
        else:
            break    
    save_list(all_cards)
    

        
if __name__ == "__main__":
    main()
