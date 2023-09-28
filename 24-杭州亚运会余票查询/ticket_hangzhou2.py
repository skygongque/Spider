import requests
import time
import json
import pandas as pd 
import numpy as np 
from tqdm import tqdm
import hashlib
import copy

""" 
纯python版本
"""

def get_index(page):
    params = {
        'sortType' :'2',
        'page': str(page),
        'pageSize' :'36',
        'langType': '1'
    }
    url = 'https://gtpapi.hangzhou2022.cn/rest/guide/project/list/queryList' # sortType=2&page=2&pageSize=36&langType=1
    ts,sign = get_ts_sign(params)
    payload = {}
    headers = {
        'authority': 'gtpapi.hangzhou2022.cn',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        # 'cookie': 'cna=l/mlG/R1Q10CAXrugBH3OgNY; xlly_s=1; _trs_uv=lmzusca5_4982_edl7; Hm_lvt_9095c4973fefa1f89e883fab90d1ff1e=1695704684; Hm_lpvt_9095c4973fefa1f89e883fab90d1ff1e=1695704684; MZCONSUMERJSESSIONID17481=TICKETMZGTP0ac9530cad2040be80dba6b70a509337; XSRF-TOKEN=9190242d-76f0-4e26-9c9f-a0b52a55225e; isg=BKKiVM-kM-_9-C7MxI7PYLO98ygE86YNwPmUmuwbgZRsvzk51IKgHYR56_tDrx6l',
        'origin': 'https://ticket.hangzhou2022.cn',
        'referer': 'https://ticket.hangzhou2022.cn/',
        'sign': sign,
        'site': 'pc',
        'siteversion': 'standard',
        'timestamp': str(ts),
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    }
    response = requests.get(url,params=params, headers=headers, data=payload)
    response.raise_for_status
    return response.json()

def parse_index(res_json):
    dataList = res_json['data']['projectPager']['dataList']
    projectId_list = [item['projectId'] for item in dataList]
    return projectId_list

def get_detail(params):
    url = "https://gtpapi.hangzhou2022.cn/rest/guide/project/detail/query" # ?projectId=216990009&langType=1
    ts,sign = get_ts_sign(params)
    payload = {}
    headers = {
        'authority': 'gtpapi.hangzhou2022.cn',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        # 'cookie': 'cna=l/mlG/R1Q10CAXrugBH3OgNY; xlly_s=1; _trs_uv=lmzusca5_4982_edl7; Hm_lvt_9095c4973fefa1f89e883fab90d1ff1e=1695704684; Hm_lpvt_9095c4973fefa1f89e883fab90d1ff1e=1695704684; MZCONSUMERJSESSIONID17481=TICKETMZGTP0ac9530cad2040be80dba6b70a509337; XSRF-TOKEN=9190242d-76f0-4e26-9c9f-a0b52a55225e; isg=BKKiVM-kM-_9-C7MxI7PYLO98ygE86YNwPmUmuwbgZRsvzk51IKgHYR56_tDrx6l',
        'origin': 'https://ticket.hangzhou2022.cn',
        'referer': 'https://ticket.hangzhou2022.cn/',
        'sign': sign,
        'site': 'pc',
        'siteversion': 'standard',
        'timestamp': str(ts),
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    }
    response = requests.get(url,params=params, headers=headers, data=payload)
    response.raise_for_status
    return response.json()

def parse(res_json):
    data = res_json['data']
    projectId = data['projectId']
    projectName = data['projectName']
    # print(projectId,projectName)
    seat_lefts = []
    eventList = data['eventList']
    for event in eventList:
        # print(event['allowChooseSeat'])
        if (not event['soldOut']) and event['allowChooseSeat']: # 筛选soldOut为False allowChooseSeat为True的
            seat_lefts.append(event['eventName'])
    if len(seat_lefts) > 0:
        return {
            'projectId':projectId,
            'projectName':projectName,
            'left_num':len(seat_lefts),
            'seat_lefts':seat_lefts
        }


def get_ts_sign(u):
    """ 签名 """
    ts = str(int(time.time() * 1000) -91)
    dic = copy.deepcopy(u)
    myKeys = list(dic.keys())
    myKeys.sort()
    sorted_params = {i: dic[i] for i in myKeys}
    sorted_params['timestamp'] = ts
    dic_str = json.dumps(sorted_params,separators=(',', ':'))
    m = hashlib.md5()
    m.update(dic_str.encode('utf-8'))
    sign = m.hexdigest()
    return ts,sign

def main():
    # res_json = get_detail({'projectId':'216707002','langType':'1'})
    # left_info = parse(res_json)
    print('正在进行爬取请耐心等待....')
    all_projectId_list = []
    result = []
    for page in range(1,4): # 索引页一共就三页
        res_index = get_index(page)
        projectId_list = parse_index(res_index)
        all_projectId_list += projectId_list

    all_projectId_list = list(set(all_projectId_list)) 
    print(all_projectId_list)
    for projectId in tqdm(all_projectId_list):
        res_json = get_detail({'projectId':str(projectId),'langType':'1'})
        left_info = parse(res_json)
        if left_info:
            result.append(left_info)
        time.sleep(1)
        # break
    df = pd.DataFrame(result)
    df.to_excel('余票情况2.xlsx')
    print('余票情况已存入 余票情况2.xlsx')


if __name__ == "__main__":
    main()