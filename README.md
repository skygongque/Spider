![pic](https://img.shields.io/badge/python-v3.7-green)
![pic](https://img.shields.io/badge/node-v12.16-green)
# 自己写的爬虫总结

文章可能首次发表于吾爱破解论坛，以下账户也是本人  
https://www.52pojie.cn/home.php?mod=space&uid=965057

## [微博模拟登录](introduction/weibo_login.md)

RSA/PKCS1_v1_5  
用python的pycryptodome或rsa库都可以实现  
下载验证码图片手动输入结果（若有接码平台或机器学习训练的模型可以接入）  

## [微博图片批量下载](introduction/weibo.md)

用asyncio + aiohttp异步下载图片  

## [网易云音乐评论爬虫](introduction/netease_comments.md)

params和encSecKey参数  
AES/CBC  
`pad = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16)`  
RSA/nopading  

## [网易云音乐下载](introduction/netease_music.md)

nodejs express  
params和encSecKey参数  
直接扣代码补全缺少的环境即可  
Crypto-js库用npm安装  

## [抖音web signature](https://github.com/skygongque/douyin_signature)

nodejs express puppeteer  
1.得到指定uid请求返回的tac  
2.puppeteer驱动chromium  
在console中执行签名算法得到signature  

# [喜马拉雅有声书爬虫](introduction/ximalay_node.md)

纯JavaScript爬虫  
通过fileId和ep等参数还原真实地址  
直接扣代码即可  

# [喜马拉雅模拟登录](https://github.com/skygongque/login-ximalaya)
opencv-python 识别滑块验证码的缺口识别成功率约 60-70%  
参考腾讯防水墙缺口的识别算法简单修改
因为喜马拉雅滑块没有检测轨迹，只对post的缺口位置经过简单的偏移  
可以实现此滑动验证码的突破


