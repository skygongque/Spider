// 补头
var window = {
  "navigator":{
    "userAgent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'
  }
}
var setTimeout = function(a){
  return a();
}
var document = {
  "cookie":""
}
var location = {
  "href":null,
  "pathname":null,
  "search":null
}
// 2021.2.1 测试时的代码
// 此时已经使用obfuscator 混淆了
function hash(_0x39aa76) {
  function _0x169b58(_0x3efe93, _0x303391) {
    return (_0x3efe93 & 2147483647) + (_0x303391 & 2147483647) ^ _0x3efe93 & 2147483648 ^ _0x303391 & 2147483648;
  }

  function _0x195ae4(_0x1ffd6f) {
    var _0x1d1db7 = "0123456789abcdef";
    var _0x447421 = '';

    for (var _0x39afff = 7; _0x39afff >= 0; _0x39afff--) {
      _0x447421 += _0x1d1db7["charAt"](_0x1ffd6f >> _0x39afff * 4 & 15);
    }

    return _0x447421;
  }

  function _0x2b81a9(_0x4a18c1) {
    var _0x2df6e0 = "2|0|1|5|4|3"["split"]('|');

    var _0x44a05c = 0;

    var _0x426218 = (_0x4a18c1["length"] + 8 >> 6) + 1;

    var _0x19d55f = new Array(_0x426218 * 16);

    for (var _0x559fc4 = 0; _0x559fc4 < _0x426218 * 16; _0x559fc4++) {
      _0x19d55f[_0x559fc4] = 0;
    }

    for (_0x559fc4 = 0; _0x559fc4 < _0x4a18c1["length"]; _0x559fc4++) {
      _0x19d55f[_0x559fc4 >> 2] |= _0x4a18c1["charCodeAt"](_0x559fc4) << 24 - (_0x559fc4 & 3) * 8;
    }

    _0x19d55f[_0x559fc4 >> 2] |= 128 << 24 - (_0x559fc4 & 3) * 8;
    _0x19d55f[_0x426218 * 16 - 1] = _0x4a18c1["length"] * 8;
    return _0x19d55f;
  }

  function _0x326f5f(_0x439195, _0x54c84b) {
    return _0x439195 << _0x54c84b | _0x439195 >>> 32 - _0x54c84b;
  }

  function _0x503031(_0x4c7fad, _0x641758, _0x49e24, _0xce70a1) {
    if (_0x4c7fad < 20) return _0x641758 & _0x49e24 | ~_0x641758 & _0xce70a1;
    if (_0x4c7fad < 40) return _0x641758 ^ _0x49e24 ^ _0xce70a1;
    if (_0x4c7fad < 60) return _0x641758 & _0x49e24 | _0x641758 & _0xce70a1 | _0x49e24 & _0xce70a1;
    return _0x641758 ^ _0x49e24 ^ _0xce70a1;
  }

  function _0x726dcc(_0x327499) {
    return _0x327499 < 20 ? 1518500249 : _0x327499 < 40 ? 1859775393 : _0x327499 < 60 ? -1894007588 : -899497514;
  }

  var _0x8479c7 = _0x2b81a9(_0x39aa76);

  var _0x397fac = new Array(80);

  var _0x259185 = 1732584193;

  var _0x17a453 = -271733879;

  var _0x1a31d4 = -1732584194;

  var _0x2175e8 = 271733878;

  var _0x1cad66 = -1009589776;

  for (var _0x2caf74 = 0; _0x2caf74 < _0x8479c7["length"]; _0x2caf74 += 16) {
    var _0x5e39d6 = _0x259185;
    var _0x32d507 = _0x17a453;
    var _0x215377 = _0x1a31d4;
    var _0x18cf19 = _0x2175e8;
    var _0xa43cf5 = _0x1cad66;

    for (var _0x2b2c1b = 0; _0x2b2c1b < 80; _0x2b2c1b++) {
      var _0x566693 = "2|5|1|4|3|6|0"["split"]('|');

      var _0x15cc0e = 0;

      if (_0x2b2c1b < 16) {
        _0x397fac[_0x2b2c1b] = _0x8479c7[_0x2caf74 + _0x2b2c1b];
      } else {
        _0x397fac[_0x2b2c1b] = _0x326f5f(_0x397fac[_0x2b2c1b - 3] ^ _0x397fac[_0x2b2c1b - 8] ^ _0x397fac[_0x2b2c1b - 14] ^ _0x397fac[_0x2b2c1b - 16], 1);
      }

      t = _0x169b58(_0x169b58(_0x326f5f(_0x259185, 5), _0x503031(_0x2b2c1b, _0x17a453, _0x1a31d4, _0x2175e8)), _0x169b58(_0x169b58(_0x1cad66, _0x397fac[_0x2b2c1b]), _0x726dcc(_0x2b2c1b)));
      _0x1cad66 = _0x2175e8;
      _0x2175e8 = _0x1a31d4;
      _0x1a31d4 = _0x326f5f(_0x17a453, 30);
      _0x17a453 = _0x259185;
      _0x259185 = t;
    }

    _0x259185 = _0x169b58(_0x259185, _0x5e39d6);
    _0x17a453 = _0x169b58(_0x17a453, _0x32d507);
    _0x1a31d4 = _0x169b58(_0x1a31d4, _0x215377);
    _0x2175e8 = _0x169b58(_0x2175e8, _0x18cf19);
    _0x1cad66 = _0x169b58(_0x1cad66, _0xa43cf5);
  }

  return _0x195ae4(_0x259185) + _0x195ae4(_0x17a453) + _0x195ae4(_0x1a31d4) + _0x195ae4(_0x2175e8) + _0x195ae4(_0x1cad66);
}

function go(_0x482ed2) {
  function _0x28d4cf() {
    var _0x61ae31 = window["navigator"]["userAgent"];
    var _0x3fdfd5 = ["Phantom"];

    for (var _0x484fd0 = 0; _0x484fd0 < _0x3fdfd5["length"]; _0x484fd0++) {
      if (_0x61ae31["indexOf"](_0x3fdfd5[_0x484fd0]) != -1) {
        return true;
      }
    }

    if (window["callPhantom"] || window["_phantom"] || window["Headless"] || window["navigator"]["webdriver"] || window["navigator"]["__driver_evaluate"] || window["navigator"]["__webdriver_evaluate"]) {
      return true;
    }
  }

  if (_0x28d4cf()) {
    return;
  }

  var _0x2ea2a1 = new Date();

  function _0x1ea3fc(_0x532427, _0xd5afb9) {
    var _0x4873bd = _0x482ed2["chars"]["length"];

    for (var _0xacfcd1 = 0; _0xacfcd1 < _0x4873bd; _0xacfcd1++) {
      for (var _0x387cac = 0; _0x387cac < _0x4873bd; _0x387cac++) {
        var _0x3d5d2c = _0xd5afb9[0] + _0x482ed2["chars"]["substr"](_0xacfcd1, 1) + _0x482ed2["chars"]["substr"](_0x387cac, 1) + _0xd5afb9[1];

        if (hash(_0x3d5d2c) == _0x532427) {
          return [_0x3d5d2c, new Date() - _0x2ea2a1];
        }
      }
    }
  }

  var _0x17a8da = _0x1ea3fc(_0x482ed2['ct'], _0x482ed2["bts"]);

  if (_0x17a8da) {
    var _0x134df4;

    if (_0x482ed2['wt']) {
      _0x134df4 = parseInt(_0x482ed2['wt']) > _0x17a8da[1] ? parseInt(_0x482ed2['wt']) - _0x17a8da[1] : 500;
    } else {
      _0x134df4 = 1500;
    }

    setTimeout(function () {
      document["cookie"] = _0x482ed2['tn'] + '=' + _0x17a8da[0] + ";Max-age=" + _0x482ed2['vt'] + "; path = /";
      location["href"] = location["pathname"] + location["search"];
      
    }, _0x134df4);
  } else {
    alert("请求验证失败");
  }
}

go({
  "bts": ["1643720298.71|0|shwg", "AbpIcEJVq%2Bsw80AY9%2Fqbw%3D"],
  "chars": "ELsLmPBnVkrcCkdfnukhdA",
  "ct": "e1b12af1530e874313fc314d52035c7357b657f9",
  "ha": "sha1",
  "tn": "__jsl_clearance_s",
  "vt": "3600",
  "wt": "1500"
});
console.log(document.cookie)

// node环境与浏览器环境一致
// 1643720298.71|0|shwgsAAbpIcEJVq%2Bsw80AY9%2Fqbw%3D
// __jsl_clearance_s=1643720298.71|0|shwgsAAbpIcEJVq%2Bsw80AY9%2Fqbw%3D;Max-age=3600; path = /
