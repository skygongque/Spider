# frida Hook 相关代码总结

### python文件中代码

```
import frida
import sys

device = frida.get_remote_device()
# 选择app的包名
session = device.attach("com.douban.frodo")

def on_message(message, data):
    if message["type"] == "send":
        print("[+] {}".format(message["payload"]))
    else:
        print("[-] {}".format(message))

src = open("hook.js",encoding='utf-8').read()

script = session.create_script(src)
script.on("message", on_message)
script.load()
sys.stdin.read()
```
### hook.js中代码
## 采坑总结

- 核心的hook逻辑在`hook.js`中  
- 使用`Java.use()`来使用java中的包  
- 若hook的函数有多个重载，使用`overload()`中传入数据类型  
- 若要打印复杂的数据类型 而不是[object Object]   

HashMap和Map类型  
```
var Map = Java.use('java.util.HashMap');
var args_x = Java.cast(x, Map);
send(args_x.toString());
```
byte[]类型  
```
var arr = Java.use("java.util.Arrays");
var JavaString =Java.use("java.lang.String");
send("参数对应数组:" + arr.toString(x))
send("参数对应字符串:" + JavaString.$new(x))
```

## 简单完整示例 hook.js

### 示例一 hook HMACHash 获取加密前后
```
setImmediate(function(){
    Java.perform(function(){
        send("starting script");        
        // var Activity = Java.use("com.douban.frodo.network.ApiSignatureHelper");
        // 定位到要hook的类名
        var HMACHash1 = Java.use("com.douban.frodo.utils.crypto.HMACHash1");
        send(HMACHash1);
        // hook 这个类的a 方法
        HMACHash1.a.implementation = function(str, str2){
            var result = HMACHash1.a(str, str2);
            send("str4:"+str);
            send(str2);
            send("加密后："+result);
            return result;
        };     
    });
});
```


### 示例二  打印android.util.Pair类型的数据
```
setImmediate(function () {
    Java.perform(function () {
        send("starting script");
        // var Activity = Java.use("com.douban.frodo.network.ApiSignatureHelper");
        // 定位到要hook的类名
        var ApiSignatureHelper = Java.use("com.douban.frodo.network.ApiSignatureHelper");
        var Pair = Java.use("android.util.Pair");
        send(ApiSignatureHelper);
        // hook 这个类的a 方法 
        ApiSignatureHelper.a.overload('java.lang.String', 'java.lang.String', 'java.lang.String').implementation = function (str1, str2, str3) {
            send(str1);
            send(str2);
            send(str3);
            var result = ApiSignatureHelper.a(str1, str2, str3);
            // 转成对应的数据类型再toString
            var args_x = Java.cast(result, Pair);
            send(args_x.toString());
            return result;
        };
    });
});
```

### 示例二 hook StringBuilder的toString
可以同正则筛选  
```
setImmediate(function () {
    Java.perform(function () {
        send("starting script");
        // var crypto = Java.use("bubei.tingshu.lib.aly.c");
        var StringBuilder = Java.use('java.lang.StringBuilder');
        var toString = StringBuilder.toString;
        toString.implementation = function () {
            var result = toString.call(this);
            var partial = '';
            if (result !== null) {
                partial = result.toString().replace('\n', '');
            }
            // hook StringBuilder的toString方法，并通过正则筛选要打印的信息
            if (partial.search(/yyting/) != -1) {
                console.log('StringBuilder.toString(); => ' + partial);
            }
            return result;
        };
    });
});
```

[frida复杂类型参数打印、参数转换、调用栈打印](https://blog.csdn.net/weixin_35762183/article/details/106802647)