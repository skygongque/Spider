# 微博图片批量下载

# install
`
pip3 install -r requirements.txt
`

# 介绍
weibo_photo.py 用requests获得图片的链接存于result.json（非重点）  
weibo_photo_dl.py 用asyncio + aiohttp异步下载result.json中jpg格式的图片  
MYretry.py 利用装饰器实现异步请求的重试（非异步可以使用retrying库）

# 可能的问题
1.只对client_exceptions.ServerDisconnectedError进行了处理  
若在请求中出现其他异常可以添加到
@MYretry(client_exceptions.ServerDisconnectedError,otherexception)  
2.不谈weibo_photo.py获取链接是同步方式，
单是weibo_photo_dl.py也有一种异步和同步代码杂糅的感觉，不知aiofiles这样用是否可以实现异步的文件写入  


代码不具备通用性，当前的功能是批量下载鞠婧祎的微博相册图片（jpg），
如需采集其他用户需要改weibo_photo.py得到新的result.json文件


# 效果
经过简单的异常处理没有遗漏的
并发数CONCURRENCY为5我家的垃圾网络用了400s下载了1500多张图
（非并发情况下等一张图片的响应就要超过1s）可以说协程的效果还不错



