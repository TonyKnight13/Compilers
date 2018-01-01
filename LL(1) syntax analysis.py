'''
LL(1)文法分析器
python 3.6.1
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
    ('F', '('): '(E)',
    ('E', ')'): 'synch',
    ('E', '$'): 'synch',
    ('T', '+'): 'synch',
    ('T', ')'): 'synch',
    ('T', '$'): 'synch',
    ('F', '*'): 'synch',
    ('F', '+'): 'synch',
    ('F', ')'): 'synch',
    ('F', '$'): 'synch'
}
# 终结符集合
ts = ('i', '(', '+', '*', ')')
# 非终结符集合
ns = ('E', 'A', 'T', 'B', 'F')


def predictiveAnalysis(strin):
    # 栈和指针
    stack = []
    mate = []
    location = 0
    # 将$压入栈中
    stack.append('$')
    # 将文法的开始符号压入栈
    stack.append('E')
    # 将输入串第一个字符读入a中
    a = strin[location]
    # 令X等于栈顶符号
    X = stack[-1]
    flag = True
    out = 1

    while flag:
        if X == a:
            if(a != '$'):
                location += 1
                a = strin[location]
                m = stack.pop()
                mate.append(m)
                print('匹配', a)
        elif X in ts:
            stack.pop()
            out = 0
            print('错误，栈顶为终结符')
        elif (X, a) not in pat.keys() and a in ts:
            location += 1
            a = strin[location]
            out = 0
            print('错误，略过')
        elif (X, a) in pat.keys():
            k = (X, a)
            if pat[k] == 'Error':
                return 0
            elif pat[k] == 'synch':
                Y = stack.pop()
                out = 0
                print('错误，', k, '= synch   ' + Y + '已经被弹出栈')
            else:
                yStr = pat[k][::-1]
                ao = stack.pop()
                print('输出' + ao + '->' + pat[k])
                for i in range(len(yStr)):
                    if(yStr[i] != '#'):
                        stack.append(yStr[i])
        else:
            location += 1
            a = strin[location]
            out = 0
            print('此符号非预测分析表终结符')
        X = stack[-1]
        if X == '$':
            flag = False
    return out


def init(strin):
    '''
    输入串的初始化，尾部加上$
    '''
    strin = strin + '$'
    return strin


str = 'i+++i'
str = init(str)
out = predictiveAnalysis(str)
if out == 1:
    print("串合法")
else:
    print("串不合法")
