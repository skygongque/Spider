const parser = require("@babel/parser");
const traverse = require("@babel/traverse").default;
const t = require("@babel/types");
const generator = require("@babel/generator").default;
const fs = require('fs');//文件系统的依赖一般都要用就一并引用了

// var jscode = `_0x1491=['\x77\x35\x58\x43\x6a\x33\x54\x43\x6b\x77\x77\x3d','\x63\x63\x4f\x6e\x4a\x56\x30\x6d','\x77\x36\x59\x53\x57\x38\x4f\x4f\x77\x6f\x6f\x3d']`
var jscode = fs.readFileSync('./source.js', {
    encoding: "utf-8"
});
var ast = parser.parse(jscode);
traverse(ast, {
	StringLiteral: delExtra,
	NumericLiteral: delExtra
})

function delExtra(path) {
	var curNode = path.node;
	delete curNode.extra;
}
var { code } = generator(ast, {
	jsescOption: {
		// 自动转义
		// minimal: true,
		// 禁止自动格式化(针对反调试)
        compact: true
	}
});
console.log(code)
fs.writeFileSync('./result/01-result.js', code, {
	encoding: "utf-8"
})