const parser = require("@babel/parser");
const traverse = require("@babel/traverse").default;
const t = require("@babel/types");
const generator = require("@babel/generator").default;
// var { decryptStr, decryptStrFnName } = require('./module01');
const fs = require('fs');//文件系统的依赖一般都要用就一并引用了

var jscode = fs.readFileSync('./result/01-result.js', {
    encoding: "utf-8"
});

// 使用parse将js转为ast语法树
var ast = parser.parse(jscode);

// 提取解密函数及解密函数名，返回去掉前3个节点后的ast对象
ast = step1(ast)
// 调用解密函数、十六进制文本还原，返回解密后的ast对象或写入还原后的代码
ast = step2(ast)

function step1(ast) {
    // 提取前3个节点的源代码及单独提取出atob函数，返回去掉前3个节点后的ast对象

    // 提取program.body下前3个节点，即提取出解密代码
    var decrypt_code = ast.program.body.slice(0, 3)
    // 剩下的节点
    var rest_code = ast.program.body.slice(3)

    // 将前3个节点替换进ast
    ast.program.body = decrypt_code
    var { code } = generator(ast, {
        // 禁止自动格式化(针对反调试)
        compact: true
    })
    // 将前3个节点的源代码赋值到全局变量中，供第二步使用
    global_code = code
    // 解密函数名(str)，供第二步使用
    decryptStr = decrypt_code[2].declarations[0].id.name

    // 提取atob函数，后面可能会做判断
    var flag = true
    const visitor = {
        "ExpressionStatement"(path) {
            path.traverse({
                "StringLiteral"(_path) {
                    delete _path.node.extra
                },
                MemberExpression: formatMember
            })
            var code = path.toString()
            if (flag && code.indexOf("atob") != -1) {
                atob_node = path.node
                flag = false
            }
        }
    }
    traverse(ast, visitor)
    ast.program.body = [atob_node]
    var { code } = generator(ast, {
        jsescOption: {
            // 自动转义
            minimal: true,
        }
    })
    const comment = "// atob函数，后面可能会判断其是否存在，勿删！"
    atob_code = comment + "\n!" + code + "\n"

    // 将剩下的节点替换进ast供后面还原
    ast.program.body = rest_code
    return ast
}
function step2(ast) {
    // 调用解密函数、十六进制文本还原
    // 返回解密后的ast对象或写入还原后的代码
    console.log("还原解密函数中...")
    // 利用eval将前3个节点的代码导入到环境中
    eval(global_code)
    traverse(ast, {
        CallExpression: funToStr,
        StringLiteral: delExtra,
        NumericLiteral: delExtra,
    })
    console.log("解密函数还原完成！")
    return ast
    
    function funToStr(path) {
        var node = path.node;
        // 判断节点类型及函数名，不是则返回
        if (!t.isIdentifier(node.callee, { name: decryptStr }))
            return;
        // 调用解密函数
        let value = eval(path.toString())
        // 是否打印
        console.log("还原前：" + path.toString(), "还原后：" + value);
        path.replaceWith(t.valueToNode(value));
    }
    function delExtra(path) {
        // 十六进制文本还原
        delete path.node.extra;
    }
}

// 使用traverse遍历语法树，因为方法的调用为CallExpression类型，所以我们只对type为CallExpression的节点进行处理。
// 类型的查看方式看代码后面的图。
// traverse(ast, { CallExpression: funToStr })
// function funToStr(path) {
//     var curNode = path.node;
//     if (curNode.callee.name === decryptStrFnName && curNode.arguments.length === 2) {
//         var strC = decryptStr(curNode.arguments[0].value, curNode.arguments[1].value);
//         //将匹配到的位置 的 方法调用 使用replaceWith方法 替换为字符串。   
//         path.replaceWith(t.stringLiteral(strC))
//     }
// }


var { code } = generator(ast, {
	jsescOption: {
		// 自动转义
		minimal: true,
	}
});


console.log(code)
fs.writeFileSync('./result/02-result.js', code, {
	encoding: "utf-8"
})




function formatMember(path) {
    // 将_0x19882c['removeCookie']['toString']()改成_0x19882c.removeCookie.toString()
    var curNode = path.node;
    if (!t.isStringLiteral(curNode.property))
        return;
    if (curNode.computed === undefined || !curNode.computed === true)
        return;
    curNode.property = t.identifier(curNode.property.value);
    curNode.computed = false;
}
