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