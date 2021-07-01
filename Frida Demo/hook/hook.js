setImmediate(function () {
    Java.perform(function () {
        send("starting script");
        // var Activity = Java.use("com.douban.frodo.network.ApiSignatureHelper");
        // 定位到要hook的类名
        var ApiSignatureHelper = Java.use("com.douban.frodo.network.ApiSignatureHelper");
        var Pair = Java.use("android.util.Pair");
        send(ApiSignatureHelper);
        // hook 这个类的a 方法 如果有多个重载的方法通过overload 传入变量的类型
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
