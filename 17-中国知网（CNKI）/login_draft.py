import requests
from PIL import Image
import re

requests.packages.urllib3.disable_warnings()


sess = requests.session()

url = "https://login.cnki.net/TopLoginNew/api/loginapi/IpLogin?isAutoLogin=true&checkCode=&isForceLogin=true&p=2&vc=%7C0&_=1625586211994 "
default_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Referer': 'https://www.cnki.net/',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
}
download_headers = {
    # 'Host': 'kns.cnki.net',# 这个字段不能加
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en;q=0.7',
}
response = sess.get(url, headers=default_headers)

print(response.text)
print(sess.cookies)

download_src = 'https://kns.cnki.net/KNS8/download?filename=0MkWWl3MxJGeYFjR29WSRBXRhN0R0EXQXplbwg3ZCVVSFNjcJdjMrp3KWpGRyM0R4hlc0c1RvF2cQRWRwJkaD5kaHBTbBl3ZvR2aXVEc6dnaZVTWRFTTTB1TM9me3cnVSBVUHBHOlV1SYdGUGtWRtZ1UklTNQFmW&tablename=CAPJLAST'


# https://kdoc.cnki.net/kdoc/download.aspx?filename=mdMp3KGlFMGlWYFx2MWdnM4o1ZGl0Ttl3capWNol2TlplcLpHaD5kTqVnVtVTT0UWW1Z3brNVcn5WW=0zdwkmQtBXcCZmb2Q0YqVDUod3c6JUMP9yKTRDSjZ2TaJUVuFmVxoXSoh1Q0VWatNUanJkeRVzTV9&tablename=CJFDAUTO&uid=&t=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhcHBpZCI6IjI5MjU4IiwidGltZXN0YW1wIjoxNjI1NTg2ODQ2LCJub25jZSI6ImxZUkY2b0N3eEwifQ.YOFuPyEzNlwatKlBjZkQ0oSURpfSxsTlKEc6M5CEyck&lang=gb

def getRedirectUrl(url: str, sess: object) -> str:
    """
    :rtype: str
    """
    response = sess.get(url, headers=default_headers,
                        verify=False, allow_redirects=False)
    return dict(response.headers).get("Location")


def requestDownloadUrl(url, sess):
    # 请求该url 被设置cookie
    response = sess.get(url, headers=default_headers)
    # /kdoc/request/ValidateCode.ashx?t=1577242936454
    return 'https://kdoc.cnki.net/kdoc/request/ValidateCode.ashx?t=1577242936454'


def postDownloadUrl(url, sess, vcode, referer):
    print(url)
    payload = f'vcode={str(vcode)}'
    print(payload)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': referer,
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Origin': 'https://kdoc.cnki.net',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = sess.post(url, headers=headers, data=payload)
    if response.headers['Content-Type'] == 'application/caj':
        with open('test.caj', 'wb') as f:
            f.write(response.content)
            f.close()
    else:
        print(response.text)


def saveCaptcha(url, sess, referer):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': referer,
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    response = sess.get(url, headers=headers)
    with open('currentCaptcha.jpg', 'wb') as f:
        f.write(response.content)
        f.close()


if __name__ == '__main__':
    redirectUrl = getRedirectUrl(download_src, sess)
    print('redirecturl', redirectUrl)
    # https://kdoc.cnki.net/kdoc/download.aspx?filename=0MkWWl3MxJGeYFjR29WSRBXRhN0R0EXQXplbwg3ZCVVSFNjcJdjMrp3KWpGRyM0R4hlc0c1RvF2cQRWRwJkaD5kaHBTbBl3ZvR2aXVEc6dnaZVTWRFTTTB1TM9me3cnVSBVUHBHOlV1SYdGUGtWRtZ1UklTNQFmW&tablename=CAPJLAST&uid=&t=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhcHBpZCI6IjI5MjU4IiwidGltZXN0YW1wIjoxNjI1OTI1MzkxLCJub25jZSI6IkgwZGx5RllLT0sifQ.WFTJAbv1ukrTghSk7fCRV78xKeERJV3rBUIBFhpz0sA&lang=gb
    # https://kdoc.cnki.net/kdoc/download.aspx?filename=kdycXQVl1TL9yS280arUVQyUTMYlzVvRXUaNzcZhTaah1czlHTiFGZMNDTxlWUqJDcCJmUYRUS5NXc=0TR5cjaOd3T0cmbxVESxs2MvMUb4UkY0YUe2FlRIlEW1FnUMp1c3N0crNzRYhHOSl3NxE2dXNmTkx&tablename=CJFD9899&uid=&t=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhcHBpZCI6IjI5MjU4IiwidGltZXN0YW1wIjoxNjI1OTIzMzIzLCJub25jZSI6InBzTDZsalBhOUgifQ.vjQ_XuJfD1HmY9yMfsd4Pe2RImE0CaotoJPbxHVu94c&lang=gb
    requestDownloadUrl(redirectUrl, sess)
    saveCaptcha(
        'https://kdoc.cnki.net/kdoc/request/ValidateCode.ashx?t=1577242936454', sess, redirectUrl)
    # Image.open('currentCaptcha.jpg')
    vcode = input('输入验证码:')
    postDownloadUrl(redirectUrl, sess, vcode, redirectUrl)
