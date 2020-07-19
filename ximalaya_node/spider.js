/* 需要会员登录后的token，仅限vip，非vip的搜索一下一大把 */

const superagent = require('superagent');
const CryptoJS = require('crypto-js');
const decrypt_xm = require('./ximalaya_decrypt2');
const fs = require('fs');


var tools = {
    get_time: function () {
        return new Date().getTime()
    },
    get_server_time: async function () {
        res = await superagent.get('https://www.ximalaya.com/revision/time')
            .set({
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'
            })
        return res.text
    },
    p: function (t) {
        return ~~(Math.random() * t)
    },

}

async function get_xm_sign() {
    /* 获取xm_sign */
    var server_time = await tools.get_server_time()
    var hash = CryptoJS.MD5(`himalaya-${server_time}`);
    var sign = `${hash}(${tools.p(100)})${server_time}(${tools.p(100)})${tools.get_time()}`
    return sign;
}

async function getTracksList(albumId, pageNum) {
    var url = `https://www.ximalaya.com/revision/album/v1/getTracksList?albumId=${albumId}&pageNum=${pageNum}`
    var xm_sign = await get_xm_sign();
    var res = await superagent.get(url, xm_sign)
        .set({
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36',
            'xm-sign': xm_sign
        })
    return res.body
}

async function track_pay(trackId) {
    /* 验证有无收听的权限 */
    var url = `https://mpay.ximalaya.com/mobile/track/pay/${trackId}?device=pc&isBackend=true&_=${tools.get_time()}`
    var xm_sign = await get_xm_sign();
    var track_pay_res = await superagent.get(url, xm_sign)
        .set({
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36',
            'xm-sign': xm_sign,
            'cookie': YouCookie
        })
    return track_pay_res.text
}


async function get_total_page(albumId) {
    var TracksList = await getTracksList(albumId, 1);
    var trackTotalCount = TracksList.data.trackTotalCount
    console.log(`共${trackTotalCount}集`)
    total_page = Math.floor(Number(trackTotalCount) / 30) + 1
    console.log(`共${total_page}页`)
    return total_page

}

function downloadFileAsync(uri, dest) {
    /* 下载文件 */
    return new Promise((resolve, reject) => {
        // 确保dest路径存在
        const file = fs.createWriteStream(dest);
        var res_data = superagent.get(uri).set(
            { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36' }
        )

        file.on('finish', () => {
            console.log(`${dest.slice(0, 3)} finish downlording`)
            file.close(resolve);
        }).on('error', (err) => {
            fs.unlink(dest);
            reject(err.message);
        })
        res_data.pipe(file);

    });
}



async function get_one_page(albumId, pageNum, start_index) {
    var TracksList = await getTracksList(albumId, pageNum)
    var list = TracksList.data.tracks
    for (var i = 0; i < list.length; i++) {
        var title = list[i].title;
        title = title.replace(/[&/|///*^%$'"#@/-]/g, "");
        var index = list[i].index;
        var trackId = list[i].trackId;
        if (index < start_index) {
            /* 跳过start_index前的下载 */
            continue
        }
        var track_pay_res = await track_pay(trackId);
        var isAuthorized = JSON.parse(track_pay_res).isAuthorized;
        if (isAuthorized) {
            console.log('start downlording', index, title);
            var whole_src = decrypt_xm.get_whole_url(track_pay_res)
            var index_string = index + ''
            /* 填充index */
            index_string = index_string.padStart(3, '0')
            var name = index_string + ' ' + title + '.m4a'
            // await downloadFileAsync(whole_src, name)
            
            /* 几乎同时发起两个下载请求，等待第二个返回后发起下两个 */
            if(i % 2===0){
                downloadFileAsync(whole_src,name)
            }else{
                await downloadFileAsync(whole_src,name)
            }

        }else{
            console.log('isAuthorized is false')
            console.log('无法下载，请确认YouCookie(1&_token)正确，或尝试重新登录后更新YouCookie')
        }

    }

}

/* 读取配置文件 */
var config = fs.readFileSync('config.json');
config = JSON.parse(config);
var YouCookie = config.YouCookie;

!async function () {
    /* albumId有声书id */
    albumId = config.albumId;
    /* start_index从第几集开始下载 */
    var start_index = config.start;
    var total_page = await get_total_page(albumId)
    console.log(`从第${start_index}集开始下载`)
    for (var i = 1; i < total_page + 1; i++) {
        await get_one_page(albumId, i, start_index)
    }

}()
