const CryptpJS = require('crypto-js');
const axios = require('axios');
/* 
网站 https://spa2.scrape.center/
使用npm安装依赖
npm install crypto-js axios
*/

function getData(limit, offset, token) {
    var config = {
        method: 'get',
        url: `https://spa2.scrape.center/api/movie/?limit=${limit}&offset=${offset}&token=${token}`,
        headers: {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
        }
    };
    axios(config)
        .then(function (response) {
            console.log(JSON.stringify(response.data));
        })
        .catch(function (error) {
            console.log(error);
        });
}

function getToken() {
    for (var t = Math.round((new Date).getTime() / 1e3).toString(),
        e = arguments.length,
        r = new Array(e), i = 0; i < e; i++)
        r[i] = arguments[i];
    r.push(t);
    var o = CryptpJS.SHA1(r.join(",")).toString(CryptpJS.enc.Hex)
        , c = CryptpJS.enc.Base64.stringify(CryptpJS.enc.Utf8.parse([o, t].join(",")));
    return c
}

function sleep(delay) {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            try {
                resolve(1)
            } catch (e) {
                reject(0)
            }
        }, delay);
    })
}

// "/api/movie"
// 10
!async function main() {
    for (var i = 0; i < 10; i++) {
        console.log(i)
        getData(10, i * 10, getToken("/api/movie", i * 10))
        await sleep(1000)
    }
}()
