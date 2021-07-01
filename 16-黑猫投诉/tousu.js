const CryptoJS = require('crypto-js');
const axios = require('axios');
/* 
目标网址：aHR0cHM6Ly90b3VzdS5zaW5hLmNvbS5jbi9jb21wYW55L3ZpZXcvP2NvdWlkPTYyNDQyMTEzNzU=
讲解： https://mp.weixin.qq.com/s/t2eoaLKuqqBRwR1dLiw3hw
*/

function getSignature(params) {
    var u = (new Date).getTime()
        , d = function (e, t, r) {
            var n = ""
                , i = t
                , a = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"];
            e && (i = Math.round(Math.random() * (r - t)) + t);
            for (var o = 0; o < i; o++) {
                n += a[Math.round(Math.random() * (a.length - 1))]
            }
            return n
        }(!1, 16)
        , l = "$d6eb7ff91ee257475%";
    var couid = params.couid;
    var page_size = params.page_size;
    var page = params.page;
    return {
        ts: u,// timestamp
        rs: d,// random string
        couid: couid,
        page_size: page_size,
        page: page,
        // SHA256 哈希
        signature: CryptoJS.SHA256([u, d, l, couid, 1, page_size, page].sort().join("")).toString()
    }
}

async function getData(params){
    var t = getSignature(params);
    var config = {
        method: 'get',
        // url: 'https://tousu.sina.com.cn/api/company/received_complaints?ts=1614340290475&rs=I66jvmc7WhlW1wOE&signature=a5c5f96f03b397bf45566a07faa959fa473b7ba65e1000dc6714ad12ab97d75f&couid=6384912431&type=1&page_size=10&page=1',
        url: `https://tousu.sina.com.cn/api/company/received_complaints?ts=${t.ts}&rs=${t.rs}&signature=${t.signature}&couid=${t.couid}&type=1&page_size=${t.page_size}&page=${t.page}`,
        headers: {
            'authority': 'tousu.sina.com.cn',
            'accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'
        }
    };
    try{
        var response  = await axios(config);
        return JSON.stringify(response.data)
    }catch(e){
        return e; 
    }
}

!async function(){
    var params = {
        couid: 6384912431,
        // couid:6244211375,
        page_size: 10,
        page: 1
    }
    var data = await getData(params);
    console.log(data)
}()