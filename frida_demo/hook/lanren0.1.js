
setImmediate(function(){
    Java.perform(function(){
        send("starting script");        
        var md5 = Java.use("bubei.tingshu.lib.aly.c.f");
        send(md5);
        // hook 这个类的a 方法
        md5.a.implementation = function(str){
            send("加密前:"+str);
            // send("加密后:"+md5.a(str));
            // return md5.a(str);
            var result = md5.a.call(this,str);
            send(result);
            return result;
        };     
    });
});