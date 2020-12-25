import requests
import json
from pyquery import PyQuery as pq
import os
import re


def open_links():
    with open('links_tmp.json', 'r', encoding='utf-8') as f:
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
        print('made dir to save img')

def parse_detail(html,title):
    doc = pq(html)
    # <div class="rich_media_content " id="js_content" style="visibility: hidden;">
    js_content = doc.find('#js_content')
    js_content.attr('style', "visibility: visible;")
    rich_pages = doc.find('.rich_pages')
    count = 0
    print('start to save img...')
    for each in rich_pages.items():
        count += 1
        origin_src = each.attr['data-src']
        src_name = str(count)+'.png'
        src_name = os.path.join(title+'_img',src_name)
        each.attr('data-src', src_name)
        each.attr('src', src_name)
        downlord_png(src_name,origin_src)
        # print(each)
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
    '''.format(js_code,content)
    with open(title+'.html','w',encoding='utf-8') as f:
        f.write(temp)
        f.close()
    print('finished saving',title)


def main():
    link_list = open_links()
    keys_name = list(link_list.keys())
    for title in keys_name:
        title_modified = re.sub('[////:/*/?/"<>|]','',title,re.S)
        print(title_modified)
        create_img_folder(title_modified+'_img')
        html = get_html(link_list[title])
        parse_detail(html,title_modified)


if __name__ == "__main__":
    main()
