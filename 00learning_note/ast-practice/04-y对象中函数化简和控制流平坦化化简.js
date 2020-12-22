const parser = require("@babel/parser");
const traverse = require("@babel/traverse").default;
const t = require("@babel/types");
const generator = require("@babel/generator").default;
// var { decryptStr, decryptStrFnName } = require('./module01');
const fs = require('fs');//文件系统的依赖一般都要用就一并引用了

const { y } = require('./result/module_y');


var jscode = fs.readFileSync('./result/03-result-move-y2module.js', {
    encoding: "utf-8"
});
// 使用parse将js转为ast语法树
var ast = parser.parse(jscode);

traverse(ast, { MemberExpression: fun2str, });
traverse(ast, { CallExpression: simplifyFunc, });
// 反控制流平坦化
traverse(ast, {WhileStatement: {exit: [replaceWhile]},});

/* 
y 中字符串替换
*/
function fun2str(path){
    var node = path.node;
    if (!t.isIdentifier(node.object))
        return;
    if (node.object.name != "y")
        return;
    if (!t.isLiteral(node.property))
        return;
    let _value = node.property.value;
    if (typeof(y[_value]) === "string"){
        path.replaceWith(t.valueToNode(y[_value]));
    }
}

/* 
1.第一个参数作为函数名，其余参数作为函数值的化简
2.两个参数的简单加减乘除或位移运算的化简
*/
function simplifyFunc(path) {
    var node = path.node;
    if (!t.isMemberExpression(node.callee))
        return;
    if (node.callee.object.name != "y")
        return;
    let _value = node.callee.property.value;
    if (!typeof (y[_value]) === "function") return;
    let ast_temp = parser.parse("var temp = " + y[_value].toString());
    // 传入y执行后的函数体的ast_temp和path
    handleSimplifyFunc(ast_temp, path)
}

function handleSimplifyFunc(ast_temp, pre_path) {
    //pre_path CallExpression 的树
    //y中对于函数的ast ast_temp
    traverse(ast_temp, {
        ReturnStatement: function (_path) {
            let _node = _path.node;
            let create_node;
            if (t.isCallExpression(_node.argument) && t.isIdentifier(pre_path.node.arguments[0])){
                // 创建一个新的函数调用
                create_node = t.callExpression(
                    pre_path.node.arguments[0],
                    pre_path.node.arguments.slice(1)//去除第一个后的作为参数
                )
            }else if (t.isBinaryExpression(_node.argument) &&　pre_path.node.arguments.length ===2){
                let left = pre_path.node.arguments[0];
                let right = pre_path.node.arguments[1];
                // 创建一个新的binaryExpression
                create_node = t.binaryExpression(_node.argument.operator, left, right);
            }else{
                return;
            }
            pre_path.replaceWith(create_node)
        },
    })
}


function replaceWhile(path) {
    // 反控制流平坦化    
    var node = path.node;
    // 判断是否是目标节点   
    if (!(t.isBooleanLiteral(node.test) || t.isUnaryExpression(node.test)))
        // 如果while中不为true或!![]
        return;
    if (!(node.test.prefix || node.test.value))
        // 如果while中的值不为true
        return;
    if (!t.isBlockStatement(node.body))
        return;
    var body = node.body.body;
    if (!t.isSwitchStatement(body[0]) || !t.isMemberExpression(body[0].discriminant) || !t.isBreakStatement(body[1]))
        return;

    // 获取数组名及自增变量名
    var swithStm = body[0];
    var arrName = swithStm.discriminant.object.name;
    var argName = swithStm.discriminant.property.argument.name
    let arr = [];

    // 找到path节点的前一个兄弟节点，即数组所在的节点，然后获取数组  
    let all_presibling = path.getAllPrevSiblings();
    // console.log(all_presibling)
    all_presibling.forEach(pre_path => {
        const { declarations } = pre_path.node;
        let { id, init } = declarations[0]
        if (arrName == id.name) {
            // 数组节点
            arr = init.callee.object.value.split('|');
            pre_path.remove()
        }
        if (argName == id.name) {
            // 自增变量节点
            pre_path.remove()
        }
    })

    // SwitchCase节点集合     
    var caseList = swithStm.cases;
    // 存放按正确顺序取出的case节点   
    var resultBody = [];
    arr.map(targetIdx => {
        var targetBody = caseList[targetIdx].consequent;
        // 删除ContinueStatement块(continue语句)     
        if (t.isContinueStatement(targetBody[targetBody.length - 1]))
            targetBody.pop();
        resultBody = resultBody.concat(targetBody)
    });
    path.replaceInline(resultBody);
}


var { code } = generator(ast, {
	jsescOption: {
		// 自动转义
		minimal: true,
	}
});

console.log(code)
fs.writeFileSync('./result/04-result.js', code, {
	encoding: "utf-8"
})