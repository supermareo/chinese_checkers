# coding=utf-8

from pythonds.basic.stack import Stack


# 后缀表达式进行计算
def calc_suffix_expression(follow):
    num = []
    base_opt = ['+', '-', '*', '/']
    for j in follow:
        if j.isdigit():
            num.append(int(j))
        if j in base_opt:
            num2 = num.pop()
            num1 = num.pop()
            if j == "+":
                num.append(num1 + num2)
            elif j == "-":
                num.append(num1 - num2)
            elif j == "*":
                num.append(num1 * num2)
            else:
                num.append(num1 / num2)
    return num[0]


def infix_to_postfix(infix_str):
    prec = {"*": 3, "/": 3, "+": 2, "-": 2, "(": 1}
    op_stack = Stack()
    postfix_list = []
    token_list = infix_str.split()
    print(token_list)
    for token in token_list:
        if token in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' or token in "0123456789":
            postfix_list.append(token)
        elif token == '(':
            op_stack.push(token)
        elif token == ')':
            top_token = op_stack.pop()
            while top_token != '(':
                postfix_list.append(top_token)
                top_token = op_stack.pop()
        else:
            while (not op_stack.isEmpty()) and \
                    (prec[op_stack.peek()] >= prec[token]):
                postfix_list.append(op_stack.pop())
            op_stack.push(token)

    while not op_stack.isEmpty():
        postfix_list.append(op_stack.pop())
    return postfix_list


# 预处理中缀表达式
def pre_process_infix_expression(infix_expression_str):
    # 去除空格
    infix_expression_str = infix_expression_str.replace(' ', '')
    infix_expression_str = infix_expression_str.replace('+', ' + ')
    infix_expression_str = infix_expression_str.replace('-', ' - ')
    infix_expression_str = infix_expression_str.replace('*', ' * ')
    infix_expression_str = infix_expression_str.replace('/', ' / ')
    infix_expression_str = infix_expression_str.replace('(', ' ( ')
    infix_expression_str = infix_expression_str.replace(')', ' ) ')
    infix_expression_str = infix_expression_str.replace('  ', ' ')
    return infix_expression_str.strip()


# 中缀表达式字符串-即我们常规四则运算
def calc(infix_expression_str):
    try:
        # 预处理
        infix_expression_str = pre_process_infix_expression(infix_expression_str)
        if infix_expression_str is None:
            return None
        suffix_expression_str = infix_to_postfix(infix_expression_str)
        return calc_suffix_expression(suffix_expression_str)
    except:
        return None
# if __name__ == '__main__':
#     # print(infix_to_postfix('8 - 7 - 1'))
#     print(calc('8-4*(7-1)/2'))
