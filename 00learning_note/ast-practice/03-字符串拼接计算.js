const parser = require("@babel/parser");
const traverse = require("@babel/traverse").default;
const t = require("@babel/types");
const generator = require("@babel/generator").default;
// var { decryptStr, decryptStrFnName } = require('./module01');
const fs = require('fs');//文件系统的依赖一般都要用就一并引用了

var jscode = fs.readFileSync('./result/02-result.js', {
    encoding: "utf-8"
});

// 使用parse将js转为ast语法树
var ast = parser.parse(jscode);
traverse(ast, { VariableDeclarator: { exit: [merge_obj] }, });  // 将拆分的对象重新合并
console.log("开始对象替换，可能稍慢，请耐心等待...");
traverse(ast, { VariableDeclarator: { exit: [callToStr] }, });  // 对象替换
traverse(ast, { ExpressionStatement: convParam, });           // 自执行实参替换形参
traverse(ast, { BinaryExpression: eval_constant,});           // 常量计算

function merge_obj(path) {
    // 将拆分的对象重新合并
    const { id, init } = path.node;
    if (!t.isObjectExpression(init))
        return;

    let name = id.name;
    let properties = init.properties;

    let scope = path.scope;
    let binding = scope.getBinding(name);
    if (!binding || binding.constantViolations.length > 0) {
        return;
    }
    let paths = binding.referencePaths;
    paths.map(function (refer_path) {
        let bindpath = refer_path.parentPath;
        if (!t.isVariableDeclarator(bindpath.node)) return;
        let bindname = bindpath.node.id.name;
        bindpath.scope.rename(bindname, name, bindpath.scope.block);
        bindpath.remove();
    });
    scope.traverse(scope.block, {
        AssignmentExpression: function (_path) {
            const left = _path.get("left");
            const right = _path.get("right");
            if (!left.isMemberExpression())
                return;
            const object = left.get("object");
            const property = left.get("property");
            if (object.isIdentifier({ name: name }) && property.isStringLiteral() && _path.scope == scope) {
                properties.push(t.ObjectProperty(t.valueToNode(property.node.value), right.node));
                _path.remove();
            }
            if (object.isIdentifier({ name: name }) && property.isIdentifier() && _path.scope == scope) {
                properties.push(t.ObjectProperty(t.valueToNode(property.node.name), right.node));
                _path.remove();
            }
        }
    })
}
function callToStr(path) {
    // 将对象进行替换
    var node = path.node;

    if (!t.isObjectExpression(node.init))
        return;

    // 获取对象内所有属性
    var objPropertiesList = node.init.properties;

    if (objPropertiesList.length == 0)
        return;

    // 对象名
    var objName = node.id.name;
    // 是否可删除该对象：发生替换时可删除，否则不删除
    var del_flag = false

    objPropertiesList.forEach(prop => {
        var key = prop.key.value;
        if (t.isFunctionExpression(prop.value)) {
            var retStmt = prop.value.body.body[0];

            // 该path的最近父节点
            var fnPath = path.getFunctionParent();
            fnPath.traverse({
                CallExpression: function (_path) {
                    if (!t.isMemberExpression(_path.node.callee))
                        return;

                    var _node = _path.node.callee;
                    if (!t.isIdentifier(_node.object) || _node.object.name !== objName)
                        return;
                    if (!(t.isStringLiteral(_node.property) || t.isIdentifier(_node.property)))
                        return;
                    if (!(_node.property.value == key || _node.property.name == key))
                        return;
                    // if (!t.isStringLiteral(_node.property) || _node.property.value != key)
                    //     return;

                    var args = _path.node.arguments;

                    // 二元运算
                    if (t.isBinaryExpression(retStmt.argument) && args.length === 2) {
                        _path.replaceWith(t.binaryExpression(retStmt.argument.operator, args[0], args[1]));
                    }
                    // 逻辑运算
                    else if (t.isLogicalExpression(retStmt.argument) && args.length == 2) {
                        _path.replaceWith(t.logicalExpression(retStmt.argument.operator, args[0], args[1]));
                    }
                    // 函数调用
                    else if (t.isCallExpression(retStmt.argument) && t.isIdentifier(retStmt.argument.callee)) {
                        _path.replaceWith(t.callExpression(args[0], args.slice(1)))
                    }
                    del_flag = true;
                }
            })
        }
        else if (t.isStringLiteral(prop.value)) {
            var retStmt = prop.value.value;

            // 该path的最近父节点
            var fnPath = path.getFunctionParent();
            fnPath.traverse({
                MemberExpression: function (_path) {
                    var _node = _path.node;
                    if (!t.isIdentifier(_node.object) || _node.object.name !== objName)
                        return;
                    if (!(t.isStringLiteral(_node.property) || t.isIdentifier(_node.property)))
                        return;
                    if (!(_node.property.value == key || _node.property.name == key))
                        return;
                    // if (!t.isStringLiteral(_node.property) || _node.property.value != key)
                    //     return;

                    _path.replaceWith(t.stringLiteral(retStmt))
                    del_flag = true;
                }
            })
        }
    });
    if (del_flag) {
        // 如果发生替换，则删除该对象
        path.remove();
    }
}
function convParam(path) {
    // 自执行函数实参替换形参
    var node = path.node;

    if (!t.isCallExpression(node.expression))
        return;

    if (node.expression.arguments == undefined || node.expression.callee.params == undefined || node.expression.arguments.length > node.expression.callee.params.length)
        return;

    var argumentList = node.expression.arguments;
    var paramList = node.expression.callee.params;
    for (var i = 0; i < argumentList.length; i++) {
        var argumentName = argumentList[i].name;
        var paramName = paramList[i].name;

        path.traverse({
            MemberExpression: function (_path) {
                var _node = _path.node;
                if (!t.isIdentifier(_node.object) || _node.object.name !== paramName)
                    return;

                _node.object.name = argumentName;
            }
        });
    }
    node.expression.arguments = [];
    node.expression.callee.params = [];
}
function eval_constant(path) {
    // 常量计算
    if (path.type == "UnaryExpression") {
        const { operator, argument } = path.node;
        if (operator == "-" && t.isLiteral(argument)) {
            return;
        }
    }
    const { confident, value } = path.evaluate();
    // 无限计算则退出，如1/0与-(1/0)
    if (value == Infinity || value == -Infinity)
        return;
    confident && path.replaceWith(t.valueToNode(value));
}


var { code } = generator(ast, {
	jsescOption: {
		// 自动转义
		minimal: true,
	}
});

console.log(code)
fs.writeFileSync('./result/03-result.js', code, {
	encoding: "utf-8"
})