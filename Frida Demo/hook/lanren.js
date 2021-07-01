setImmediate(function () {
    Java.perform(function () {
        send("starting script");
        var c_class = Java.use('bubei.tingshu.lib.aly.c.c');
        var a_method = c_class.a;
        var Map = Java.use('java.util.TreeMap');
        a_method.overload('java.lang.String', 'java.util.Map').implementation = function (arg1,arg2) {
            var args_x = Java.cast(arg2, Map);
            send(arg1);
            send(args_x.toString());
            return a_method(arg1,arg2);
            // var result = a_method(this,arguments);
            // send(result);
            // return result;
        }
    });
});