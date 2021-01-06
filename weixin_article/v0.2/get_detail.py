import requests
import json
from pyquery import PyQuery as pq
import os
import re
from pictureDownloader.picturedown import AsyncDownloader
import asyncio


loop = asyncio.get_event_loop()

def open_links():
    with open('articleLinks.json', 'r', encoding='utf-8') as f:
        return json.loads(f.read())


def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text


def downlord_png(name, src):
    with open(name, 'wb') as f:
        res = requests.get(src)
        f.write(res.content)


def create_img_folder(name):
    if not os.path.exists(name):
        os.makedirs(name)
        print('Made dir to save img')


def parse_detail(html, title):
    """
    调整图片的属性为可见，使用 asyncio + aiohttp 异步下载图片
    """
    doc = pq(html)
    js_content = doc.find('#js_content')
    js_content.attr('style', "visibility: visible;")
    rich_pages = doc.find('.rich_pages')
    url_list = []
    for count,each in enumerate(rich_pages.items()):
        origin_src = each.attr['data-src']
        url_list.append(origin_src)
        src_name = str(count).zfill(4)+'.png'
        src_name = os.path.join(title+'_img', src_name)
        each.attr('data-src', src_name)
        each.attr('src', src_name)
        # downlord_png(src_name, origin_src)
    # 改为异步下载图片 提高效率
    print('start to save img...')
    save_path = title+'_img'
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    ad = AsyncDownloader(save_path)
    # 把任务推入事件循环
    loop.run_until_complete(ad.asyncTasks(url_list))
    content = doc('.rich_media_area_primary_inner').html()
    js_code = '''
<script>
    window.onload = function(){
        var js_content = document.getElementById('js_content')
        js_content.style.fontStyle ='normal'
    }
</script>
    '''
    temp = '''
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    {}
</head>
<body>
    {}
</body>
</html>
    '''.format(js_code, content)
    with open(title+'.html', 'w', encoding='utf-8') as f:
        f.write(temp)
        f.close()
    print('finished saving', title)


def main():
    link_list = open_links()
    keys_name = list(link_list.keys())
    for title in keys_name:
        try:
            title_modified = re.sub('[////:/*/?/"<>|]', '', title, re.S)
            print(title_modified)
            create_img_folder(title_modified+'_img')
            html = get_html(link_list[title])
            parse_detail(html, title_modified)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()
