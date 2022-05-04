// md5_str = "da4eaf0fbeb3213d9b164b1c855aa855\u0000"
md5_str = "d44bf7751588dce3d0b8c5908c00ff92\u0000"
var result_arr = []
var p = 0;
for (var i = md5_str.length-1; i >= 0 ;i-- ){
    if (i % 3 == 0){
        p = p + 1;
        if (p > 4) {
            p = p - 4
        }
        let a =  md5_str.charCodeAt(i+2);
        let b =  md5_str.charCodeAt(i+1);
        let c =  md5_str.charCodeAt(i);
        if (p == 1){
            result_arr.push(demo1(a,b,c))
        }else if(p == 2){
            result_arr.push(demo5(a,b,c))
        }else if(p == 3){
            result_arr.push(demo9(a,b,c))
        }else if(p == 4){
            result_arr.push(demo13(a,b,c))
        }
        console.log('p',p)
        console.log(i)
        
        console.log('==================')
    }
}
console.log(result_arr.join(''))

function demo1 (a,b,c){
    // 32 31 30
    let x1 = b << 8;
    let x2 = a ^ 42;
    let x3 = x2 | x1;
    let x4 = c << 16;
    let x5 = x3 | x4;
    var f_str = "RuPtXwxpThIZ0qyz_9fYLCOV8B1mMGKs7UnFHgN3iDaWAJE-Qrk2ecSo6bjd4vl5"
    return ""+ f_str[x5 % 64] + f_str[(x5 >> 6) % 64] + f_str[(x5 >> 12) % 64] + f_str[(x5 >> 18) % 64]
}
function demo5 (a,b,c){
    // 29 28 27
    let x1 = b ^ 42;
    let x2 = x1 << 8;
    let x3 = a | x2;
    let x4 = c << 16;
    let x5 = x3 | x4;
    var f_str = "RuPtXwxpThIZ0qyz_9fYLCOV8B1mMGKs7UnFHgN3iDaWAJE-Qrk2ecSo6bjd4vl5"
    return ""+  f_str[x5 % 64] + f_str[(x5 >> 6) % 64] + f_str[(x5 >> 12) % 64] + f_str[(x5 >> 18) % 64]
}

function demo9 (a,b,c){
    // 26 25 24
    let x1 = b << 8;
    let x2 = a | x1;
    let x3 = (c ^ 42) << 16;
    let x4 = x2 | x3;
    var f_str = "RuPtXwxpThIZ0qyz_9fYLCOV8B1mMGKs7UnFHgN3iDaWAJE-Qrk2ecSo6bjd4vl5"
    return ""+ f_str[x4 % 64] + f_str[(x4 >> 6) % 64] + f_str[(x4 >> 12) % 64] + f_str[(x4 >> 18) % 64]
}

function demo13(a,b,c){
    // 23 22 21
    let x1 = b << 8;
    let x2 = a | x1;
    let x3 = c << 16;
    let x4 = x2 | x3;
    var f_str = "RuPtXwxpThIZ0qyz_9fYLCOV8B1mMGKs7UnFHgN3iDaWAJE-Qrk2ecSo6bjd4vl5"
    return ""+ f_str[x4 % 64] + f_str[(x4 >> 6) % 64] + f_str[(x4 >> 12) % 64] + f_str[(x4 >> 18) % 64]
}