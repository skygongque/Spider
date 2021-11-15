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
