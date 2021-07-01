# ast 还原混淆代码笔记

## 安装

``` 
npm install @babel/core
```

## 引入依赖
```
const parser = require("@babel/parser");
const traverse = require("@babel/traverse").default;
const t = require("@babel/types");
const generator = require("@babel/generator").default;
const fs = require('fs');//文件系统的依赖一般都要用就一并引用了
```

## 例子1 还原16进制字符
```
traverse(ast, {
	StringLiteral: delExtra,
	NumericLiteral: delExtra
})

function delExtra(path) {
	var curNode = path.node;
	delete curNode.extra;
}
``` 


