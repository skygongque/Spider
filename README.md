![pic](https://img.shields.io/badge/python-v3.7-green)
![pic](https://img.shields.io/badge/node-v12.16-green)
# 自己写的爬虫总结

文章可能首次发表于吾爱破解论坛，以下账户也是本人  
https://www.52pojie.cn/home.php?mod=space&uid=965057

## [微博模拟登录](微博登录/introduction.MD)

RSA/PKCS1_v1_5  
用python的pycryptodome或rsa库都可以实现  
下载验证码图片手动输入结果 可以接入深度学习的[验证码识别模型](https://github.com/skygongque/captcha-weibo)准确率98%以上  

## [微博图片批量下载](微博图片)

用asyncio + aiohttp异步下载图片  

## [网易云音乐评论爬虫](网易音乐评论)

params和encSecKey参数  
AES/CBC  
`pad = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16)`  
RSA/nopading  

## [网易云音乐下载](网易音乐)

nodejs express  
params和encSecKey参数  
直接扣代码补全缺少的环境即可  
Crypto-js库用npm安装  

## [抖音web signature](https://github.com/skygongque/douyin_signature)

~~目前官方自己的**web端**也无法访问用户主页，无法得到tac参数，**所以该方法已经失效**，可以尝试逆向抖音的app。~~

~~通过补环境的方式得到可以在node环境单独运行的签名算法，需要tac参数（网页端源码中获取）。~~

相关环境的补充

```
Audio = {}
document = {
    createElement: function() {
        return canvas
    }
};
canvas = {
    getContext: function getContext() {
        return CanvasRenderingContext2D
    },
    toDataURL: function toDataURL() {
        return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADAAAAAQCAYAAABQrvyxAAACyUlEQVRIS8XWTYhVZRgH8N8dkPFqJqgI4sKmTUSgaBCKihCI5dZFUEaLwHAThjujEnXjpkAUHSRc+AEtFJIWKWRBSR9QENgiggplNqkTlXBnhjveeM6cF955PXccFJ2zuPec99zz3v/X87+3ZfrRK67jslWvxb103vCxx770DN5sApSAloBLco+SzFKcxbZClmG8gw7uIdCkfnq+BDsXbmzEizhYg2p0oEn1PEK5II/SgTKPbXyE89iBt+oPDDcpWz7cbwZysq/h9Vqd9/E2fkWsn0GsJeVi/1DvE6xJQLJoNA1T7PN0wx73zMBMDsTGTXMQ1n6TAfkJ63ACr+IcDmekUr6D0FUkdb+uc18SCPCba4ILitlodGA2ik8R7Rmw2E4ThnR9oVsRjJyuxL/4FLdwJCOQE07O5CBjQONIRINk7l4iOOMQB4mkdn6eajWgM2mhYU855KhRXRMO6DqKD/Ay3sWygkCKUE6qJPAegmis3+5T0I0EEtj8PUVn+r2e+Zb52HqjPqti8ptFnnPHPhzH6lq5+KIcbOwX4AJkAtjkQK50Pi9pfWfEKR/ifjVaOjC1wcLq9ZoPXbTLZfyi7Vljlep/4nSd8ZzA9bpNokUuzYJASTSBT3Mzcr8qbO77CNBSk0ZNGrPHoO+r1plnta4YxhxcTiAAbMcPs3QgXLpSC1EmKfbd38+B/jMQ4NvuWoTlPnfNKfyIES3P142U12Y/B6oI1Kj6RSgcOIZX6lqe0YHyL0Su/tT5gJ5JbSt03PSfrl34vco//2i522fgHma5/M1Ie20KZ0oHEsj5Fhireqijra2j4wlL3HHMGrv9bC2+tKUGf1vLxMOgfNBnp89AT8sGq3xrHE/WVRo0ojQHvWSHK/Y6ab83qhz/gZsYr34V5uAoCQwYstV1F6zzlXlaxg0aMeQvq7zgqu+qno+WuYG/5xJ86PU//5znHgwZKlQAAAAASUVORK5CYII="
    },
}

CanvasRenderingContext2D = {
    arc: function arc() {},
    stroke: function stroke() {},
    fillText: function fillText() {},
}
window = {
    document: {
        location:{},
        _zid:2
    },
}
```



~~nodejs express puppeteer   
1.得到指定uid请求返回的tac  
2.puppeteer驱动chromium  
在console中执行签名算法得到signature~~ 

## [喜马拉雅有声书爬虫](喜马拉雅)

纯JavaScript爬虫  
通过fileId和ep等参数还原真实地址  
直接扣代码即可  

## [喜马拉雅模拟登录](https://github.com/skygongque/login-ximalaya)
opencv-python 识别滑块验证码的缺口识别成功率约 60-70%  
参考腾讯防水墙缺口的识别算法简单修改
因为喜马拉雅滑块没有检测轨迹，只对post的缺口位置经过简单的偏移  
可以实现此滑动验证码的突破

## 58同城
密码加密RSA
有浏览器指纹  

## 豆瓣app _sig
> frida 简单使用  

[安装frida环境](./Frida Demo/installFrida.md)   
[豆瓣app _sig 分析](./Frida Demo/doubanAppSigHook.md)    
[frida 相关代码总结](./Frida Demo/hooksnippets.md)  

## 猫眼电影字体反爬
[猫眼电影字体反爬](https://github.com/skygongque/knn-font)  
使用knn（k近邻算法）  
字体文件的标注使用font creator 软件 


## 百度翻译
[百度翻译](19-百度翻译/fanyiBaidu.MD)  


