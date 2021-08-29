# 网易云音乐下载
截止2021.8.29有效  

## 使用方法
1. 安装crypto-js等依赖  
```
npm install
```
2. 运行main.py
```
python main.py
```


## 网易云加密的核心代码如下
使用AES/CBC加密歌曲id等信息  
使用RSA加密AES的密钥  

```
/* 核心加密过程从此处开始 */
!function() {
    function a(a) {
        // 函数a 用于产生随机字符串
        var d, e, b = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", c = "";
        for (d = 0; a > d; d += 1)
            e = Math.random() * b.length,
            e = Math.floor(e),
            c += b.charAt(e);
        return c
    }
    function b(a, b) {
        // 函数b AES 加密
        var c = CryptoJS.enc.Utf8.parse(b)
          , d = CryptoJS.enc.Utf8.parse("0102030405060708")
          , e = CryptoJS.enc.Utf8.parse(a)
          , f = CryptoJS.AES.encrypt(e, c, {
            iv: d, // 偏移值
            mode: CryptoJS.mode.CBC  //CBC工作模式
        });
        return f.toString()
    }
    function c(a, b, c) {
        // RSA加密
        var d, e;
        return setMaxDigits(131),
        d = new RSAKeyPair(b,"",c),
        e = encryptedString(d, a)
    }
    function d(d, e, f, g) {
        // 核心加密函数
        var h = {}
          , i = a(16);
        return h.encText = b(d, g),//"0CoJUm6Qyw8W8jud" 为密钥的AES 加密 歌曲的id等信息
        h.encText = b(h.encText, i),//函数a 产生的16位字符为密钥的AES 二次加密 歌曲的id等信息
        h.encSecKey = c(i, e, f),//ras 加密a 产生的16位字符(即二次AES加密的密钥)
        h//return 后逗号隔开顺序执行，最后只返回最后一个逗号后内容
    }
    function e(a, b, d, e) {
        var f = {};
        return f.encText = c(a + e, b, d),
        f
    }
    asrsea = d,
    ecnonasr = e
}();
```

## 其他
分别使用`execjs`和`express`搭建服务两种方法运行js代码，生成所需参数给python使用。