var magic = {}
function my_test(e, t, r) {
    "use strict";
    // r.d(t, "a", (function() {
    //     return z
    // }
    // ));
    const n = "3.7.2"
      , i = n
      , a = "function" === typeof atob
      , o = "function" === typeof btoa
      , s = "function" === typeof Buffer
      , u = "function" === typeof TextDecoder ? new TextDecoder : void 0
      , c = "function" === typeof TextEncoder ? new TextEncoder : void 0
      , l = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
      , f = Array.prototype.slice.call(l)
      , h = (e=>{
        let t = {};
        return e.forEach((e,r)=>t[e] = r),
        t
    }
    )(f)
      , d = /^(?:[A-Za-z\d+\/]{4})*?(?:[A-Za-z\d+\/]{2}(?:==)?|[A-Za-z\d+\/]{3}=?)?$/
      , p = String.fromCharCode.bind(String)
      , m = "function" === typeof Uint8Array.from ? Uint8Array.from.bind(Uint8Array) : (e,t=(e=>e))=>new Uint8Array(Array.prototype.slice.call(e, 0).map(t))
      , v = e=>e.replace(/=/g, "").replace(/[+\/]/g, e=>"+" == e ? "-" : "_")
      , _ = e=>e.replace(/[^A-Za-z0-9\+\/]/g, "")
      , y = e=>{
        let t, r, n, i, a = "";
        const o = e.length % 3;
        for (let s = 0; s < e.length; ) {
            if ((r = e.charCodeAt(s++)) > 255 || (n = e.charCodeAt(s++)) > 255 || (i = e.charCodeAt(s++)) > 255)
                throw new TypeError("invalid character found");
            t = r << 16 | n << 8 | i,
            a += f[t >> 18 & 63] + f[t >> 12 & 63] + f[t >> 6 & 63] + f[63 & t]
        }
        return o ? a.slice(0, o - 3) + "===".substring(o) : a
    }
      , g = o ? e=>btoa(e) : s ? e=>Buffer.from(e, "binary").toString("base64") : y
      , b = s ? e=>Buffer.from(e).toString("base64") : e=>{
        const t = 4096;
        let r = [];
        for (let n = 0, i = e.length; n < i; n += t)
            r.push(p.apply(null, e.subarray(n, n + t)));
        return g(r.join(""))
    }
      , w = (e,t=!1)=>t ? v(b(e)) : b(e)
      , k = e=>{
        if (e.length < 2) {
            var t = e.charCodeAt(0);
            return t < 128 ? e : t < 2048 ? p(192 | t >>> 6) + p(128 | 63 & t) : p(224 | t >>> 12 & 15) + p(128 | t >>> 6 & 63) + p(128 | 63 & t)
        }
        t = 65536 + 1024 * (e.charCodeAt(0) - 55296) + (e.charCodeAt(1) - 56320);
        return p(240 | t >>> 18 & 7) + p(128 | t >>> 12 & 63) + p(128 | t >>> 6 & 63) + p(128 | 63 & t)
    }
      , T = /[\uD800-\uDBFF][\uDC00-\uDFFFF]|[^\x00-\x7F]/g
      , M = e=>e.replace(T, k)
      , S = s ? e=>Buffer.from(e, "utf8").toString("base64") : c ? e=>b(c.encode(e)) : e=>g(M(e))
      , E = (e,t=!1)=>t ? v(S(e)) : S(e)
      , x = e=>E(e, !0)
      , L = /[\xC0-\xDF][\x80-\xBF]|[\xE0-\xEF][\x80-\xBF]{2}|[\xF0-\xF7][\x80-\xBF]{3}/g
      , A = e=>{
        switch (e.length) {
        case 4:
            var t = (7 & e.charCodeAt(0)) << 18 | (63 & e.charCodeAt(1)) << 12 | (63 & e.charCodeAt(2)) << 6 | 63 & e.charCodeAt(3)
              , r = t - 65536;
            return p(55296 + (r >>> 10)) + p(56320 + (1023 & r));
        case 3:
            return p((15 & e.charCodeAt(0)) << 12 | (63 & e.charCodeAt(1)) << 6 | 63 & e.charCodeAt(2));
        default:
            return p((31 & e.charCodeAt(0)) << 6 | 63 & e.charCodeAt(1))
        }
    }
      , O = e=>e.replace(L, A)
      , D = e=>{
        if (e = e.replace(/\s+/g, ""),
        !d.test(e))
            throw new TypeError("malformed base64.");
        e += "==".slice(2 - (3 & e.length));
        let t, r, n, i = "";
        for (let a = 0; a < e.length; )
            t = h[e.charAt(a++)] << 18 | h[e.charAt(a++)] << 12 | (r = h[e.charAt(a++)]) << 6 | (n = h[e.charAt(a++)]),
            i += 64 === r ? p(t >> 16 & 255) : 64 === n ? p(t >> 16 & 255, t >> 8 & 255) : p(t >> 16 & 255, t >> 8 & 255, 255 & t);
        return i
    }
      , C = a ? e=>atob(_(e)) : s ? e=>Buffer.from(e, "base64").toString("binary") : D
      , Y = s ? e=>m(Buffer.from(e, "base64")) : e=>m(C(e), e=>e.charCodeAt(0))
      , P = e=>Y(N(e))
      , j = s ? e=>Buffer.from(e, "base64").toString("utf8") : u ? e=>u.decode(Y(e)) : e=>O(C(e))
      , N = e=>_(e.replace(/[-_]/g, e=>"-" == e ? "+" : "/"))
      , R = e=>j(N(e))
      , I = e=>{
        if ("string" !== typeof e)
            return !1;
        const t = e.replace(/\s+/g, "").replace(/={0,2}$/, "");
        return !/[^\s0-9a-zA-Z\+/]/.test(t) || !/[^\s0-9a-zA-Z\-_]/.test(t)
    }
      , F = e=>({
        value: e,
        enumerable: !1,
        writable: !0,
        configurable: !0
    })
      , H = function() {
        const e = (e,t)=>Object.defineProperty(String.prototype, e, F(t));
        e("fromBase64", (function() {
            return R(this)
        }
        )),
        e("toBase64", (function(e) {
            return E(this, e)
        }
        )),
        e("toBase64URI", (function() {
            return E(this, !0)
        }
        )),
        e("toBase64URL", (function() {
            return E(this, !0)
        }
        )),
        e("toUint8Array", (function() {
            return P(this)
        }
        ))
    }
      , B = function() {
        const e = (e,t)=>Object.defineProperty(Uint8Array.prototype, e, F(t));
        e("toBase64", (function(e) {
            return w(this, e)
        }
        )),
        e("toBase64URI", (function() {
            return w(this, !0)
        }
        )),
        e("toBase64URL", (function() {
            return w(this, !0)
        }
        ))
    }
      , U = ()=>{
        H(),
        B()
    }
      , z = {
        version: n,
        VERSION: i,
        atob: C,
        atobPolyfill: D,
        btoa: g,
        btoaPolyfill: y,
        fromBase64: R,
        toBase64: E,
        encode: E,
        encodeURI: x,
        encodeURL: x,
        utob: M,
        btou: O,
        decode: R,
        isValid: I,
        fromUint8Array: w,
        toUint8Array: P,
        extendString: H,
        extendUint8Array: B,
        extendBuiltins: U
    }
    magic.encodeURL = x
}

my_test()
// magic.encodeURL('2wfirM0Ws/oGgBk1mhmF8eRstUkDCRTGhe/2/NtzFaQ=')
function my_encode(e){
    return magic.encodeURL(e)
}
