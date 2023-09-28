# 杭州亚运会余篇筛选

不是抢票！不是抢票！不是抢票！

杭州亚运会的官方售票网站是 https://ticket.hangzhou2022.cn/ 

但是似乎没有筛选余票的功能，所有项目都标着可选座但是点进去却没有票，好烦，因此有了这个小项目。

核心判断逻辑是筛选 soldOut为False allowChooseSeat为True的项目存入Excel中

# 使用方法
## 安装依赖
```
pip install -r requirements.txt
```
(可选)安装node.js环境

## 运行
纯python实现版本
```
python ticket_hangzhou2.py
```
execjs 运行js版本
```
python ticket_hangzhou.py
```

运行后会生成 `余票情况.xlsx` 筛选`left_num` 大于1的项目即为有余票的项目

# 不准确的情况

本程序的核心判断逻辑是筛选 soldOut为False allowChooseSeat为True的项目
```python
# 筛选soldOut为False allowChooseSeat为True的项目
if (not event['soldOut']) and event['allowChooseSeat']: 
    seat_lefts.append(event['eventName'])
```
对于`暂不可售`的情况可能存在误判  