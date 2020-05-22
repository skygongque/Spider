/* 引入crypto-js 用于aes加密 */
var CryptoJS = require('crypto-js');
function RSAKeyPair(a, b, c) {
    this.e = biFromHex(a),
    this.d = biFromHex(b),
    this.m = biFromHex(c),
    this.chunkSize = 2 * biHighIndex(this.m),
    this.radix = 16,
    this.barrett = new BarrettMu(this.m)
}
// 。。。。此处省略几百行(为RSA加密过程)需要扣取
/* 核心加密过程从此处开始 */
!function() {
    function a(a) {
        // 函数a 用于产生随机字符串
        var d, e, b = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", c = "";
        for (d = 0; a > d; d += 1)
            e = Math.random() * b.length,
            e = Math.floor(e),
            c += b.charAt(e);
        return c
    }
    function b(a, b) {
        // 函数b AES 加密
        var c = CryptoJS.enc.Utf8.parse(b)
          , d = CryptoJS.enc.Utf8.parse("0102030405060708")
          , e = CryptoJS.enc.Utf8.parse(a)
          , f = CryptoJS.AES.encrypt(e, c, {
            iv: d, // 偏移值
            mode: CryptoJS.mode.CBC  //CBC工作模式
        });
        return f.toString()
    }
    function c(a, b, c) {
        // RSA加密
        var d, e;
        return setMaxDigits(131),
        d = new RSAKeyPair(b,"",c),
        e = encryptedString(d, a)
    }
    function d(d, e, f, g) {
        // 核心加密函数
        var h = {}
          , i = a(16);
        return h.encText = b(d, g),//"0CoJUm6Qyw8W8jud" 为密钥的AES 加密 歌曲的id等信息
        h.encText = b(h.encText, i),//函数a 产生的16位字符为密钥的AES 二次加密 歌曲的id等信息
        h.encSecKey = c(i, e, f),//ras 加密a 产生的16位字符(即二次AES加密的密钥)
        h//return 后逗号隔开顺序执行，最后只返回最后一个逗号后内容
    }
    function e(a, b, d, e) {
        var f = {};
        return f.encText = c(a + e, b, d),
        f
    }
    asrsea = d,
    ecnonasr = e
}();

function get_params(ids) {
    var params = `{"ids":"${ids}","level":"standard","encodeType":"aac","csrf_token":""}","csrf_token":""}`;
    var result = asrsea(params, "010001", "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7", "0CoJUm6Qyw8W8jud");
    return result;
}
// 导出get_params方便server.js使用
module.exports = {
    get_params
}

// var ids = "[1357850926,492144016,415090367]";
// var result = get_params(ids);
// console.log(result);
/* 请求接口https://music.163.com/weapi/song/enhance/player/url/v1 */