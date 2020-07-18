import requests
import json

url = "http://jiexi.shunyiwenxiu.com/dhyjx_ver_9.1.php"

# payload = "url=https%3A%2F%2Fwww.iqiyi.com%2Fv_19rzj6uadg.html&type=&ref=0&lg=3&tm=1594907011&key=8597dd0fe2d662ff13e279ecfcdf7bc8&key2=967642c7859c07c7032de44d20fb5bd5&token=5a793791516473c2291063d35a3e7075&sdky=64c490737699b21819c2858aa9f52621"
payload = {
  'url': 'https://www.iqiyi.com/v_19rzj6uadg.html',
  'type': '',
  'ref': '0',
  'lg': '3',
  'tm': 1595041526,
  'key': '1da5a0ae904c82d1b0e5452f62528c26',
  'key2': '967642c7859c07c7032de44d20fb5bd5',
  'token': '9cc3bf2ff593d92514d3e178c22cf599',
  'sdky': '2843be738729de930538cf3e746a9a10'
}
# payload = "url=https%3A%2F%2Fwww.iqiyi.com%2Fv_19rzj6uadg.html&type=&ref=0&lg=3&tm=1595038965&key=1da5a0ae904c82d1b0e5452f62528c26&key2=967642c7859c07c7032de44d20fb5bd5&token=9cc3bf2ff593d92514d3e178c22cf599&sdky=c94caddb3d4b06176ec4d99869438411"
# 1595041867
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'http://jiexi.shunyiwenxiu.com',
    # 'Referer': 'http://jiexi.shunyiwenxiu.com/?url=https://www.iqiyi.com/v_19rzj6uadg.html&lg=3&key=300f3be3a81f886dc6fb0d5d1a3aa5c3&tm=1594998783',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en;q=0.7',
    # 'Cookie': 'time_//api.adinisp.com/ximu-9426c06e139254993a407601a15571b4.m3u8=1645.14513; domain=jiexi.shunyiwenxiu.com; time_//api.adinisp.com/ximu-6bba361eb5299c55d5c7188fd1fe2ff9.m3u8=8.768052; sky_pm=33b065aa4aa42028512ce89971773439_1594911326656; sky_pm_en=1632d5220ca4fa6c7a365cff234927cf'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
