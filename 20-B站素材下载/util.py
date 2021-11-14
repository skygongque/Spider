import requests
from tqdm import tqdm

# pip install tqdm -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
def downloadFILE(url,name):
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
    }
    resp = requests.get(url=url,stream=True,headers=headers)
    content_size = int(int(resp.headers['Content-Length'])/1024)
    with open(name, "wb") as f:
        print("Pkg total size is:",content_size,'k,start...')
        for data in tqdm(iterable=resp.iter_content(1024),total=content_size,unit='k',desc=name):
            f.write(data)
        print(name , "download finished!")

if __name__ == '__main__':
    downloadFILE('http://i0.hdslb.com/bfs/creative/1322bc1a9be43b9bcef9cdf3c83718c7e1bbec64.zip','nice')