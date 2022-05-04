md5_str = "d44bf7751588dce3d0b8c5908c00ff92\u0000"
// md5_str = 'bafff7c63d805106515ac0887d81bffc\u0000'
// "aTYyNrX0Q0NXQHYqhUF8Q6e0gqNY67YqmL2qoQH8e_FY"
// aTYyNrX0Q0NXQHYqhUF8Q6e0gqNY67YqmL2qoQH8e_FY
// aTYyNrX0Q0NXQHYqhUF8Q6e0gqNY67YqmL2qoQH8e_FY
function demo1 (a,b,c){
    // 32 31 30
    let x1 = b << 8;
    let x2 = a ^ 42;
    let x3 = x2 | x1;
    let x4 = c << 16;
    let x5 = x3 | x4;
    var f_str = "RuPtXwxpThIZ0qyz_9fYLCOV8B1mMGKs7UnFHgN3iDaWAJE-Qrk2ecSo6bjd4vl5"
    console.log(f_str[x5 % 64],f_str[(x5 >> 6) % 64],f_str[(x5 >> 12) % 64],f_str[(x5 >> 18) % 64])
}
function demo5 (a,b,c){
    // 29 28 27
    let x1 = b ^ 42;
    let x2 = x1 << 8;
    let x3 = a | x2;
    let x4 = c << 16;
    let x5 = x3 | x4;
    var f_str = "RuPtXwxpThIZ0qyz_9fYLCOV8B1mMGKs7UnFHgN3iDaWAJE-Qrk2ecSo6bjd4vl5"
    console.log(f_str[x5 % 64],f_str[(x5 >> 6) % 64],f_str[(x5 >> 12) % 64],f_str[(x5 >> 18) % 64])
}

function demo9 (a,b,c){
    // 26 25 24
    let x1 = b << 8;
    let x2 = a | x1;
    let x3 = (c ^ 42) << 16;
    let x4 = x2 | x3;
    var f_str = "RuPtXwxpThIZ0qyz_9fYLCOV8B1mMGKs7UnFHgN3iDaWAJE-Qrk2ecSo6bjd4vl5"
    console.log(f_str[x4 % 64],f_str[(x4 >> 6) % 64],f_str[(x4 >> 12) % 64],f_str[(x4 >> 18) % 64])
}

function demo13(a,b,c){
    // 23 22 21
    let x1 = b << 8;
    let x2 = a | x1;
    let x3 = c << 16;
    let x4 = x2 | x3;
    console.log(x4)
    var f_str = "RuPtXwxpThIZ0qyz_9fYLCOV8B1mMGKs7UnFHgN3iDaWAJE-Qrk2ecSo6bjd4vl5"
    console.log(f_str[x4 % 64],f_str[(x4 >> 6) % 64],f_str[(x4 >> 12) % 64],f_str[(x4 >> 18) % 64])
}


function demo17(a,b,c){
    // 20 19 18
    demo1(a,b,c)
}
function demo21(a,b,c){
    // 17 16 15
    demo5(a,b,c)
}
function demo25(a,b,c){
    // 14 13 12
    demo9(a,b,c)
}
function demo29(a,b,c){
    // 67Yq
    // 11 10 9 
    demo13(a,b,c)
}

function demo33(a,b,c){
    // mL2q
    // 8 7 6  
    demo1(a,b,c)
}

function demo37(a,b,c){
    // oQH8
    // 5 4 3
    demo5(a,b,c)
}

function demo41(a,b,c){
    // e_FY
    // 2 1 0
    demo9(a,b,c)
}



demo13(48,57,53)

demo13(56,56,48)
demo1(0,50,57)
demo1(0,99,102)
demo5(102,102,48)
demo5(102,98,49)
demo9(48,99,56)
demo9(56,100,55)

demo17(99,56,98)
demo21(48,100,51)
demo25(101,99,100)
demo29(56,56,53)
demo33(49,53,55)
demo37(55,102,98)
demo41(52,52,100)

