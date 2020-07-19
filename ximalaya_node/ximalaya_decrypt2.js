/* 2020.7.19更新 */
var J = function (t) {
    if (Array.isArray(t))
        return t
}
    , Z = function (t, e) {
        var n = []
            , r = !0
            , o = !1
            , i = void 0;
        try {
            for (var a, u = t[Symbol.iterator](); !(r = (a = u.next()).done) && (n.push(a.value),
                !e || n.length !== e); r = !0)
                ;
        } catch (t) {
            o = !0,
                i = t
        } finally {
            try {
                r || null == u.return || u.return()
            } finally {
                if (o)
                    throw i
            }
        }
        return n
    }
    , tt = function () {
        throw new TypeError("Invalid attempt to destructure non-iterable instance")
    }
    , et = function (t, e) {
        return J(t) || Z(t, e) || tt()
    }
    , nt = function (t) {
        return JSON.parse(JSON.stringify(t))
    };

function gt(t, e) {
    for (var n, r = [], o = 0, i = "", a = 0; 256 > a; a++)
        r[a] = a;
    for (a = 0; 256 > a; a++)
        o = (o + r[a] + t.charCodeAt(a % t.length)) % 256,
            n = r[a],
            r[a] = r[o],
            r[o] = n;
    for (var u = o = a = 0; u < e.length; u++)
        o = (o + r[a = (a + 1) % 256]) % 256,
            n = r[a],
            r[a] = r[o],
            r[o] = n,
            i += String.fromCharCode(e.charCodeAt(u) ^ r[(r[a] + r[o]) % 256]);
    return i
}
function bt(t) {
    this._randomSeed = t,
        this.cg_hun()
}
bt.prototype = {
    cg_hun: function () {
        this._cgStr = "";
        var t = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ/\\:._-1234567890"
            , e = t.length
            , n = 0;
        for (n = 0; n < e; n++) {
            var r = this.ran() * t.length
                , o = parseInt(r);
            this._cgStr += t.charAt(o),
                t = t.split(t.charAt(o)).join("")
        }
    },
    cg_fun: function (t) {
        t = t.split("*");
        var e = ""
            , n = 0;
        for (n = 0; n < t.length - 1; n++)
            e += this._cgStr.charAt(t[n]);
        return e
    },
    ran: function () {
        return this._randomSeed = (211 * this._randomSeed + 30031) % 65536,
            this._randomSeed / 65536
    },
    cg_decode: function (t) {
        var e = ""
            , n = 0;
        for (n = 0; n < t.length; n++) {
            var r = t.charAt(n)
                , o = this._cgStr.indexOf(r);
            -1 !== o && (e += o + "*")
        }
        return e
    }
};
var wt = gt("xm", "Ä[ÜJ=Û3Áf÷N")
    , Et = [19, 1, 4, 7, 30, 14, 28, 8, 24, 17, 6, 35, 34, 16, 9, 10, 13, 22, 32, 29, 31, 21, 18, 3, 2, 23, 25, 27, 11, 20, 5, 15, 12, 0, 33, 26]
    , Tt = function (t) {
        var e = gt(function (t, e) {
            for (var n = [], r = 0; r < t.length; r++) {
                for (var o = "a" <= t[r] && "z" >= t[r] ? t[r].charCodeAt() - 97 : t[r].charCodeAt() - "0".charCodeAt() + 26, i = 0; 36 > i; i++)
                    if (e[i] == o) {
                        o = i;
                        break
                    }
                n[r] = 25 < o ? String.fromCharCode(o - 26 + "0".charCodeAt()) : String.fromCharCode(o + 97)
            }
            return n.join("")
        }("d" + wt + "9", Et), function (t) {
            if (!t)
                return "";
            var e, n, r, o, i, a = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 62, -1, -1, -1, 63, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, -1, -1, -1, -1, -1, -1, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, -1, -1, -1, -1, -1, -1, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, -1, -1, -1, -1, -1];
            for (o = (t = t.toString()).length,
                r = 0,
                i = ""; r < o;) {
                do {
                    e = a[255 & t.charCodeAt(r++)]
                } while (r < o && -1 == e); if (-1 == e)
                    break;
                do {
                    n = a[255 & t.charCodeAt(r++)]
                } while (r < o && -1 == n); if (-1 == n)
                    break;
                i += String.fromCharCode(e << 2 | (48 & n) >> 4);
                do {
                    if (61 == (e = 255 & t.charCodeAt(r++)))
                        return i;
                    e = a[e]
                } while (r < o && -1 == e); if (-1 == e)
                    break;
                i += String.fromCharCode((15 & n) << 4 | (60 & e) >> 2);
                do {
                    if (61 == (n = 255 & t.charCodeAt(r++)))
                        return i;
                    n = a[n]
                } while (r < o && -1 == n); if (-1 == n)
                    break;
                i += String.fromCharCode((3 & e) << 6 | n)
            }
            return i
        }(t)).split("-")
            , n = et(e, 4)
            , r = n[0];
        return {
            sign: n[1],
            buy_key: r,
            token: n[2],
            timestamp: n[3]
        }
    }


// var info = {
//     albumId: 2910554,
//     apiVersion: "1.0.0",
//     authorizedType: 1,
//     buyKey: "617574686f72697a6564",
//     domain: "http://audiopay.cos.xmcdn.com",
//     downloadQualityLevel: 1,
//     duration: 1244,
//     ep: "20NvOoh6T39X3qwKO4cY5g5bVhg+gnLGS4Mce1ywDy2pmeiI3q+JneRc0f6I0qUzC+F10iAYfaVg2ez+xgwQ2rsQOCBS",
//     fileId: "19*7*20*16*24*1*56*55*28*38*56*25*64*56*37*28*56*22*43*19*2*65*49*12*13*50*41*5*0*10*49*49*8*35*34*59*38*59*41*63*48*65*59*6*1*25*21*17*59*38*30*",
//     highestQualityLevel: 2,
//     isAuthorized: true,
//     msg: "0",
//     ret: 0,
//     sampleDuration: 180,
//     sampleLength: 1559877,
//     seed: 1136,
//     title: "《唐砖》918",
//     totalLength: 10074267,
//     trackId: 22188799,
//     uid: 25256063,
// };

// var seed = info.seed;
// var fileId = info.fileId;
// var duration = info.duration;
function get_whole_url(info) {
    var info = JSON.parse(info)
    var seed = info.seed;
    var fileId = info.fileId;
    var duration = info.duration;
    var n = new bt(seed).cg_fun(fileId);
    var address = "/" === n[0] ? n : "/".concat(n);
    // console.log(address);
    var sign_etc = Tt(info.ep);
    // console.log(sign_etc);
    var whole_address1 = "".concat("https://audiopay.cos.xmcdn.com", "/download/").concat("1.0.0").concat(address)
    var whole_address = "".concat(whole_address1, "?").concat(`sign=${sign_etc.sign}&buy_key=${sign_etc.buy_key}&token=${sign_etc.token}&timestamp=${sign_etc.timestamp}&duration=${duration}`);
    // console.log(whole_address);
    return whole_address;
};

// console.log(get_whole_url(JSON.stringify(info)));
module.exports = {
    get_whole_url
}
