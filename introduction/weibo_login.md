介绍
对于爬取少量的微博信息自己手动登录再copy一下cookie是最简单的方式
而对于大规模的爬取，需要大量账号的登录，手动登录费时费力，模拟登录就有它的重要意义
一般的做法是大量账号的模拟登录并保存cookie形成cookie池，提供爬虫使用


代码参考https://github.com/CharlesPikachu/DecryptLogin/blob/master/DecryptLogin/platforms/weibo.py
通过新浪通行证的登录来登录微博https://login.sina.com.cn/signup/signin.php

登录过程
1.预登录，向prelogin_url(https://login.sina.com.cn/sso/prelogin.php)发起get请求得到rsa加密的参数
    该请求的核心参数
    su  为用户名的base64加密
    _   时间戳 python模拟 str(int(time.time()*1000))
    其他entry,rsakt,client为不变参数

2.登录，向ssologin_url(https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19))发起post请求登录
    改请求核心参数
    su 为用户名的base64加密
    servertime 预登录返回
    nonce 预登录返回
    rsakv 预登录返回
    sp servertime + '\t' +nonce +'\n'+ password 这一串字符（如图）的rsa加密
        rsa加密的modules是与请求返回的pubkey,exponent是"10001"（二进制），用PKCS1_v1_5方式填充
        rsa的加密可以用 python的RSA库模拟 也可用pycryptodome库模拟，选择PKCS1_v1_5即可



3.请求login_url(https://passport.weibo.com/wbsso/login)
    需要携带的核心参数ticket, ssosavestate，均为post请求的返回值