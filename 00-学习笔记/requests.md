# requests

## requests 保存cookies到json文件
```
# 省略了用session进行登录的代码
# 保存cookies
    with open('chongbuluo_cookies.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(session.cookies.get_dict()))
        f.close()
```

## requests 加载cookies的两种方式
- 把cookie先写成字典形式，然后把字典转换为cookiejar  
方法一  
```
# 注意：这个方法会替换掉原有的cookies
# 开启一个会话Session
s = requests.Session()
# 从chrome浏览器中取到的cookie值
cookie_dict = {
    "49BAC005-7D5B-4231-8CEA-16939BEACD67": "cktest001",
    "JSESSIONID": "F4FFF69B8XXXXXXC8DCB4C061C0",
    "JSESSIONIDSSO": "9D49C76FD6XXXXXF294242B44A",
}
# 把cookie值转换为cookiejar类型，然后传给Session
s.cookies = requests.utils.cookiejar_from_dict(
    cookie_dict, cookiejar=None, overwrite=True
)
```
方法二  
```
# 开启一个会话Session
s = requests.Session()
# 创建一个Cookie Jar对象
jar = requests.cookies.RequestsCookieJar()
# 向Cookie Jar对象中添加cookie值
jar.set("49BAC005-7D5B-4231-8CEA-1XXXXBEACD67", "cktXXXX001")
jar.set("JSESSIONID", "F4FFF69B8CXXXX80F0C8DCB4C061C0")
jar.set("JSESSIONIDSSO", "9D49C7XXXX448FDF5B0F294242B44A")
# 把cookies追加到Session中
s.cookies.update(jar)
```


> https://cloud.tencent.com/developer/article/1616038


## requests 复杂数据的post 如B站的字幕上传接口  
注意需要字符串的需要json.dumps  
但是整个payload不需要json.dumps,传入requests.post的data会自动进行urlencode编码
```
url = "https://api.bilibili.com/x/v2/dm/subtitle/draft/save"
payload = {
    "type": 1,
    "oid": cid,
    # 'oid': 257842077,
    "lan": "en",
    # subtitleData 已经是json.dumps之后的字符串
    "data": subtitleData,
    "submit": "true",
    "sign": "false",
    "csrf": "",
    "bvid": bvid
    # 'bvid': 'BV1Qa4y1p7hg'
}
headers = {
    'authority': 'api.bilibili.com',
    'accept': 'application/json, text/plain, */*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
    'content-type': 'application/x-www-form-urlencoded',
    # 'content-type': 'application/json',
    'origin': 'https://account.bilibili.com',
    'referer': 'https://account.bilibili.com/subtitle/edit/',
    'accept-language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en;q=0.7',
    'cookie': ''
}
response = requests.request("POST", url, headers=headers, data=payload)
print(response.text)
```
