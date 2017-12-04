'''
LL(1)文法分析器
'''
# 预测分析表
pat = {
    ('E', 'i'): 'TA',
    ('E', '('): 'TA',
    ('A', '+'): '+TA',
    ('A', ')'): '#',
    ('A', '$'): '#',
    ('T', 'i'): 'FB',
    ('T', '('): 'FB',
    ('B', '*'): '*FB',
    ('B', '+'): '#',
    ('B', ')'): '#',
    ('B', '$'): '#',
    ('F', 'i'): 'i',
    ('F', '('): '(E)'
}
# 终结符集合
ts = ('i', '(', '+', '*', ')')
# 非终结符集合
ns = ('E', 'A', 'T', 'B', 'F')

def predictiveAnalysis(str):
        # 栈和指针
        stack = []
        location = 0
        #将$压入栈中
        stack.append('$')
        #将文法的开始符号压入栈
        stack.append('E')
        # 将输入串第一个字符读入a中
        a = str[location]
        # 令X等于栈顶符号
        X = stack[-1]
        flag = True

        while flag:
            if X == a:
                if(a != '$'):
                    location += 1
                    a = str[location]
                stack.pop()           
            elif X in ts:
                return 0
            elif (X, a) in pat.keys():
                k = (X, a)
                if pat[k] == 'Error':
                    return 0
                else:
                    yStr = pat[k][::-1]
                    stack.pop()
                    for i in range(len(yStr)):
                        if(yStr[i] != '#'):
                            stack.append(yStr[i])   
            else:
                return 0         
            X = stack[-1]
            if X == '$':
                flag = False
        return 1

def init(str):
    '''
    输入串的初始化，尾部加上$
    '''
    str = str + '$'
    return str

str = 'i+i*i'
str = init(str)
out = predictiveAnalysis(str)
if out == 1:
    print("串合法")
else:
    print("串不合法")