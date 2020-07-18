/* 
某vip解析接口破解
该接口使用的大量反调试的方法
比如：
    - 不同类型的无限debugger
        - Function构造器触发 和 直接debugger关键字触发的
    - 对字符串进行了加密base64
    - 关键代码 got函数 处使用了控制流平坦化（绑定了自己的域名）
    - 加密逻辑就简单的加盐的MD5
*/

const CryptoJS = require('crypto-js');
const superagent = require('superagent');

var key2 = '967642c7859c07c7032de44d20fb5bd5';
// var key2 = '97719cbcf24daf3d6c8d9d002b79dc0f';
// '967642c7859c07c7032de44d20fb5bd5'
function time() {
    var _0x203c30 = {
        'QsVwb': function (_0x5e9585, _0x3f2379) {
            return _0x5e9585(_0x3f2379);
        },
        'VEGIp': function (_0x117716, _0x3a1527) {
            return _0x117716 / _0x3a1527;
        }
    };
    var _0x2a8c80 = new Date()["getTime"]();
    return _0x203c30["QsVwb"](parseInt, _0x203c30["VEGIp"](_0x2a8c80, 0x3e8));
}
console.log(time())

    ; got = function (_0x4233e5) {
        var _0x41aa1f = {
            'UVyhF': function (_0x14c943, _0x20a265) {
                return _0x14c943(_0x20a265);
            },
            'pWIEc': function (_0x1b96e5, _0x2b59a2) {
                return _0x1b96e5 + _0x2b59a2;
            },
            'MKpOV': "daheiyun1888",
            'NDWbW': "221",
            'QNEJU': function (_0x2a9536, _0x929c7c) {
                return _0x2a9536 > _0x929c7c;
            },
            'ukHSg': "jiexi.shunyiwenxiu.com",
            'VAXwx': function (_0x4e1d4b, _0x2a6747) {
                return _0x4e1d4b === _0x2a6747;
            },
            'bgnFP': "GPEdE",
            'DZUyM': function (_0x12bbcc, _0x5bf4b3) {
                return _0x12bbcc(_0x5bf4b3);
            },
            'RfjiM': function (_0x3e667c, _0x46c0da) {
                return _0x3e667c !== _0x46c0da;
            },
            'XaotG': "pOgik",
            'utZzg': "rcCBy",
            'XtzVr': function (_0x3b8d61, _0x33798d) {
                return _0x3b8d61(_0x33798d);
            },
            'lelxh': function (_0x34b284, _0x1e5ccb) {
                return _0x34b284 + _0x1e5ccb;
            }
        };
        var _0x489eeb = _0x41aa1f["MKpOV"];
        // console.log(_0x489eeb);
        // daheiyun1888
        // 221
        var _0x192279 = _0x41aa1f["NDWbW"];
        // console.log(_0x192279);
        var _0x4047f5 = "jiexi.shunyiwenxiu.com";
        if (_0x41aa1f["QNEJU"](_0x4047f5["indexOf"](_0x41aa1f["ukHSg"]), -0x1)) {
            if (_0x41aa1f["VAXwx"](_0x41aa1f["bgnFP"], _0x41aa1f["bgnFP"])) {
                // var _0x46de7c = _0x41aa1f["DZUyM"](md5, _0x41aa1f["pWIEc"](_0x4233e5, _0x489eeb));
                var _0x46de7c = CryptoJS.MD5(_0x4233e5 + _0x489eeb).toString();
                console.log(_0x489eeb)
                console.log(1)
            }
            // else {
            //     var _0x499a5d = _0x41aa1f[_0x5aa4('17', 'zJ99')](md5, _0x41aa1f[_0x5aa4('18', 'XLp&')](_0x4233e5, _0x192279));
            // }
        } else {
            if (_0x41aa1f["RfjiM"](_0x41aa1f["XaotG"], _0x41aa1f["utZzg"])) {
                var _0x46de7c = CryptoJS.MD5(_0x4233e5 + _0x192279).toString();
                console.log(2)
                // var _0x46de7c = _0x41aa1f["XtzVr"](md5, _0x41aa1f["lelxh"](_0x4233e5, _0x192279));
            } else {
                ooe["href"] = _0x41aa1f["pWIEc"](_0x41aa1f["pWIEc"](ooe["href"], '?'), i);
                console.log(3)
            }
        }
        return _0x46de7c;
    }

function got221(x) {
    return CryptoJS.MD5(x + "221").toString();
};
function got_wskjsdhfk(x) {
    return CryptoJS.MD5(x + "wskjsdhfk").toString();
};
function got_daheiyun1888(x) {
    return CryptoJS.MD5(x + "daheiyun1888").toString();
}
; got2 = function (_0x7af2cb) {
    var _0x3e3ea0 = {
        'nbFrj': function (_0x4bb0c5, _0x3b5a25) {
            return _0x4bb0c5(_0x3b5a25);
        },
        'eXOmJ': function (_0x3573b5, _0x3b5bd1) {
            return _0x3573b5 + _0x3b5bd1;
        },
        'lDSYA': "wskjsdhfk",
        'RKbRM': "daheiyun1888",
        'OvDKw': "221",
        'fhQYs': function (_0x261677, _0x4d4086) {
            return _0x261677 > _0x4d4086;
        },
        'IXExe': "jiexi.shunyiwenxiu.com",
        'hFkPq': function (_0x4459d7, _0x34a98a) {
            return _0x4459d7 !== _0x34a98a;
        },
        'uEsfh': "OUHAR",
        'agByj': function (_0xec93c3, _0x1d845c) {
            return _0xec93c3(_0x1d845c);
        },
        'qoooI': function (_0x2d5a04, _0x3bb42a) {
            return _0x2d5a04 + _0x3bb42a;
        }
    };
    var _0x478c83 = _0x3e3ea0["RKbRM"];
    var _0x3cae71 = _0x3e3ea0["OvDKw"];
    var _0x32ae4e = "jiexi.shunyiwenxiu.com";
    if (_0x3e3ea0["fhQYs"](_0x32ae4e["indexOf"](_0x3e3ea0["IXExe"]), -0x1)) {
        if (_0x3e3ea0["hFkPq"](_0x3e3ea0["uEsfh"], _0x3e3ea0["uEsfh"])) {
            return got_daheiyun1888(_0x7af2cb);

        } else {
            var _0x213af6 = got_wskjsdhfk(_0x7af2cb);
        }
    } else {
        var _0x213af6 = got221(_0x7af2cb);
    }
    return _0x213af6;
};

// var temp = got("https://www.iqiyi.com/v_19rzj6uadg.html1594907294daheiyunjiexi0614")
// var key = got(temp);
// console.log(key);

/* 输入要解析的视频地址 */
// var url = "https://www.iqiyi.com/v_19rzj6uadg.html"
var url = "https://v.youku.com/v_show/id_XMTA3MDAzNDA0.html"

// daheiyunjiexi0614
// var key = got(got(url + time() + "daheiyunjiexi0614"));
// "wskjsdhfk"
// "daheiyun1888"
// "221"
console.log("got2", got2("https://www.iqiyi.com/v_19rzj6uadg.html1594995936daheiyunjiexi0614"))
// var key = got_wskjsdhfk(got_wskjsdhfk(url + time() + "daheiyunjiexi0614"));

var key = got_daheiyun1888(got_daheiyun1888(url + time() + "daheiyunjiexi0614"));


// var key = got2(got2(url +1595038965 + "daheiyunjiexi0614"));

function get_token(text) {
    // return CryptoJS.MD5(text + "shibai").toString();
    return CryptoJS.MD5(text+"_wp6f").toString();
    // _wp6f
    // return CryptoJS.MD5(text + "wslkwodfiejkhf").toString();
};

var params = {
    'url': url,
    'type': "",
    'ref': "0",
    'lg': "3",
    'tm': time(),
    'key': key,
    'key2': key2,
    'token': get_token(key),
    'sdky': get_token(time())
}
console.log(params);

superagent.post('http://jiexi.shunyiwenxiu.com/dhyjx_ver_9.1.php')
    .send(params)
    .set({
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'http://jiexi.shunyiwenxiu.com',
        // referer和cookie不校验，随便带一个固定的
        'Referer': 'http://jiexi.shunyiwenxiu.com/?url=https://www.iqiyi.com/v_19rzj6uadg.html&lg=3&key=300f3be3a81f886dc6fb0d5d1a3aa5c3&tm=1594998783',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en;q=0.7',
        'Cookie': 'time_//api.adinisp.com/ximu-9426c06e139254993a407601a15571b4.m3u8=1645.14513; domain=jiexi.shunyiwenxiu.com; time_//api.adinisp.com/ximu-6bba361eb5299c55d5c7188fd1fe2ff9.m3u8=8.768052; sky_pm=33b065aa4aa42028512ce89971773439_1594911326656; sky_pm_en=1632d5220ca4fa6c7a365cff234927cf'
    })
    .then(res => {
        console.log(JSON.parse(res.text));
    })
