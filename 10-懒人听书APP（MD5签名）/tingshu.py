import requests
import hashlib

def get_paly_url(entityId, sections):
    token = 'HCvrt6XKdUjP1SZKF6GjFg**_5Q-vbHrlEjiKL1oDFkTxMA**'
    # frida hook得到md5前的明文，主要确定参数顺序
    sc_raw = f'/yyting/gateway/entityPath.action?entityId={str(entityId)}&entityType=3&imei=bHJpZGEzRWxwMWU1TUw5M3F4bURCcFlibURnPT0=&mode=0&nwt=1&opType=1&q=377&sections=[{str(sections)}]&token={token}&type=0iJ0DgxmdC83#I&j@iwg'
    sc = hashlib.md5(sc_raw.encode()).digest().hex()
    url = f"https://dapis.mting.info/yyting/gateway/entityPath.action?entityId={str(entityId)}&entityType=3&opType=1&sections=[{str(sections)}]&type=0&token={token}&imei=bHJpZGEzRWxwMWU1TUw5M3F4bURCcFlibURnPT0%3D&nwt=1&q=377&mode=0&sc={sc}"
    payload = {}
    headers = {
        'User-Agent': 'Android7.1.2/yyting/OPPO/PCRT00/ch_qutoutiao/214/AndroidHD',
        'Referer': 'yytingting.com',
        'ClientVersion': '6.6.3',
        'Host': 'dapis.mting.info'
    }
    response = requests.request(
        "GET", url, headers=headers, data=payload)
    print(response.text)


if __name__ == "__main__":
    entityId = 46122241
    for sections in range(1,20):
        get_paly_url(entityId,sections)