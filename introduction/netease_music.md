# 网易云音乐真实地址解析

扣取网易云音乐生成encparam,sencSecKey部分的代码  
------

用excejs 和 HTTP API (node.js + express)两种方法运行扣出来的js代码  

另外encparam,sencSecKey其实用到了AES加密和RSA加密，之前看到过完全逆向成python代码的，若利用漏洞可以跳过RSA加密的过程将更加高效。  