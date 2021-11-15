# 目标网址

```
aHR0cHM6Ly93d3cuY2l3ZWltYW8uY29tL2NoYXB0ZXIvMTAzNzUxNzIx(base64编码)
```

# 核心逻辑
/ajax_get_session_code 请求该接口绑定cookie中的ci_session和chapter_access_key  
/get_book_chapter_detail_info 请求该接口返回加密的小说数据
    解密方式是AES


# 其他
代码基本没有混淆适合练手  
典型的一类请求参数不加密相应结果加密的网址，数据的解密过程在前端
