import hashlib
import requests
import time

""" 
知乎'x-zse-96' 签名算法
source:101_3_2.0+/api/v4/search_v3?t=general&q=office&correction=1&offset=0&limit=20&filter_fields=&lc_idx=0&show_all_topics=0&search_source=Normal+"APAdT9SE4hSPTk_l1utlpb-FN6jTF5TgpSY=|1651578807"
signature:sign(md5(source))
sign方法
    1. md5(source) 后的字符串末尾补\u0000 通过charCodeAt从末尾开始得到3个数字一组的数字
    2. 3个数字作为参数通过4种位运算得到一个大数m
    3. fixed_str = "RuPtXwxpThIZ0qyz_9fYLCOV8B1mMGKs7UnFHgN3iDaWAJE-Qrk2ecSo6bjd4vl5"
        4个数字一组通过索引固定的字符串得到每组的四个字符， 比如任意一组的4个字符分别是 fixed_str[m % 64],fixed_str[(m >> 6) % 64],fixed_str[(m >> 12) % 64],fixed_str[(m >> 18) % 64]
    4. 拼接所有得到的字符串得到最后的签名
"""


def get_x_zse_96(source):
    """ 
    知乎'x-zse-96' 签名算法
    source:101_3_2.0+/api/v4/search_v3?t=general&q=go&correction=1&offset=0&limit=20&filter_fields=&lc_idx=0&show_all_topics=0&search_source=Normal+"APAdT9SE4hSPTk_l1utlpb-FN6jTF5TgpSY=|1651578807"
    x_zse_96:aM28FgL0r72xc8YyB0S0Fh90kR2XU9Y0mLxyNhU0HG2p
    """
    md5_str = hashlib.md5(source.encode()).hexdigest() + '\u0000'
    f_str = "RuPtXwxpThIZ0qyz_9fYLCOV8B1mMGKs7UnFHgN3iDaWAJE-Qrk2ecSo6bjd4vl5"
    result_arr = []
    p = 0
    for i in range(len(md5_str)-1, -1, -1):
        if i % 3 == 0:
            p += 1
            p = p - 4 if p > 4 else p
            a = ord(md5_str[i+2])
            b = ord(md5_str[i+1])
            c = ord(md5_str[i])
            # 4种 位运算的方式
            def m1(a, b, c): return ((a ^ 42) | (b << 8)) | (c << 16)
            def m2(a, b, c): return (a | ((b ^ 42) << 8)) | (c << 16)
            def m3(a, b, c): return (a | (b << 8)) | ((c ^ 42) << 16)
            def m4(a, b, c): return (a | (b << 8)) | (c << 16)
            if p == 1:
                m = m1(a, b, c)
                result_arr += [f_str[m % 64],
                               f_str[(m >> 6) % 64], f_str[(m >> 12) % 64], f_str[(m >> 18) % 64]]
            elif p == 2:
                m = m2(a, b, c)
                result_arr += [f_str[m % 64],
                               f_str[(m >> 6) % 64], f_str[(m >> 12) % 64], f_str[(m >> 18) % 64]]
            elif p == 3:
                m = m3(a, b, c)
                result_arr += [f_str[m % 64],
                               f_str[(m >> 6) % 64], f_str[(m >> 12) % 64], f_str[(m >> 18) % 64]]
            else:
                m = m4(a, b, c)
                result_arr += [f_str[m % 64],
                               f_str[(m >> 6) % 64], f_str[(m >> 12) % 64], f_str[(m >> 18) % 64]]
    return "".join(result_arr)


def test_request():
    # 签名的source大部分在url中，后面一小串在cookie中
    q = 'jsvmp'
    url = f"https://www.zhihu.com/api/v4/search_v3?t=general&q={q}&correction=1&offset=0&limit=20&filter_fields=&lc_idx=0&show_all_topics=0&search_source=Normal"
    # 1651647084
    ts = str(int(time.time()))
    source = '101_3_2.0+' + \
        url.replace('https://www.zhihu.com', '') + \
        f'+"ADAdVkmJ4xSPToECDLS545d-Sa0c7bcaTX0=|{ts}"'
    payload = {}
    headers = {
        'authority': 'www.zhihu.com',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': f'_zap=f052be32-e5c3-4716-8d66-8b5fef459e0b; _xsrf=fe108895-0c9e-4815-8efa-9e9bd17b6fd6; KLBRSID=975d56862ba86eb589d21e89c8d1e74e|1651647084|1651647083; d_c0="ADAdVkmJ4xSPToECDLS545d-Sa0c7bcaTX0=|{ts}"; ariaDefaultTheme=undefined; KLBRSID=975d56862ba86eb589d21e89c8d1e74e|1651649085|1651647083',
        # 'referer': 'https://www.zhihu.com/search?type=content&q=python'
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
        # 'x-ab-param': 'pf_adjust=0;top_test_4_liguangyi=1;tp_dingyue_video=0;qap_question_author=0;qap_question_visitor= 0;tp_zrec=1;tp_topic_style=0;pf_noti_entry_num=2;se_ffzx_jushen1=0;tp_contents=2',
        # 'x-ab-pb': 'CpQC9gIECgEJ6QSYCPQDdAhVCTQM5ArdB+ALtwM3DHYIowkxBokIDwu0AGoBYAlJClcE7Ao/AAEG6wZgCz8GQwCiAyoGJwkHCk8DxQjaCFQJTwqmBHoIAQuiBqEDjAXlCWkBSQkRBU8HdwfFCSoDJwjMCeAJBgpSC30C5QiRCcgJEgnDCWcIbAi1C7QK5wVHAOMFMAZBBpsH3AvECUIJVgw7AlADFgbMAo0EeAeyB6YG2AeNCccJzwsyBaAD4QnxCdcL9As/CasJyglAATMFeQhhCcsJVgWUBnQB0QnYAjIDiwXzA1EFhAmbC7kC1gSeBdwH9AmMBCkF1wIzBCcHyQlXBysK1giEAlIFdQkWCYsJ9gkbAMYJEooBAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAQAAAAAAGAAAAAAAAAAAAAAAAAAAAAAAAQAAAAACAAAAAAEAAAAAAAAEAAMAAAAAAAAAAAAAAQAAAAAAAAAAAAAACwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAILAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
        'x-api-version': '3.0.91',
        'x-app-za': 'OS=Web',
        'x-requested-with': 'fetch',
        'x-zse-93': '101_3_2.0',
        'x-zse-96': f'2.0_{get_x_zse_96(source)}'
    }
    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.json())


if __name__ == "__main__":
    test_request()

    # print(get_x_zse_96('101_3_2.0+/api/v4/search_v3?t=general&q=go&correction=1&offset=0&limit=20&filter_fields=&lc_idx=0&show_all_topics=0&search_source=Normal+"APAdT9SE4hSPTk_l1utlpb-FN6jTF5TgpSY=|1651578807"'))
