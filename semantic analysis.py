'''
语义分析——符号表信息登录 
python 3.6.1
'''

import collections


class s:
    '''
    词法分析输出的对象
    '''

    def __init__(self, strs, state):
        self.strname = strs
        self.state = state


class lexer:
    '''
    词法分析
    '''
    resword = {'real': '4', 'integer': '5', 'ptr': '6'}

    def __init__(self, strs):
        self.strings = strs
        self.state = -1
        self.stritemList = []

    def convert(self):
        strLength = len(self.strings)
        i = 0
        string = ''
        while i < strLength:
            ch = self.strings[i]
            i += 1
            if self.state == -1:
                if ch.isalpha():
                    self.state = 1
                    string = ch
                elif ch.isspace():
                    self.state = -1
                elif ch == ':':
                    self.state = 2
                    self.stritemList.append(s(ch, self.state))
                    self.state = -1
                elif ch == ';':
                    self.state = 3
                    self.stritemList.append(s(ch, self.state))
                    self.state = -1
                elif ch == '#':
                    self.state = 0
                    self.stritemList.append(s(ch, self.state))
                    self.state = -1
                else:
                    strItem = ch + '字符不可识别'
                    self.state = -1
            elif self.state == 1:
                if ch.isalpha() or ch.isdigit():
                    string += ch
                    self.state = 1
                else:
                    if string in self.resword.keys():
                        self.state = self.resword.get(string)
                    strItem = string
                    self.stritemList.append(s(strItem, self.state))
                    string = ''
                    self.state = -1
                    i -= 1

    def getstritemList(self):
        return self.stritemList


class stitem:
    '''
    符号表的表项
    '''

    def __init__(self, name, typename, offset):
        self.name = name
        self.typename = typename
        self.offset = offset


class tbl:
    '''
    符号表
    '''
    tbl = collections.OrderedDict()  # 有序字典

    def __init__(self, width=None):
        self.width = width

    def pop(self):  # 栈的pop操作
        popitem = self.tbl.popitem()
        return popitem

    def push(self, item):  # 栈的push操作
        self.tbl[item.name] = item


def mktable(previous):
    '''
    创建一张新的符号表，并返回指向新表的指针。参数previous指向先前创建的符号，放在新符号表的表头。
    '''
    table = tbl()
    if previous.name == '':
        return table
    else:
        table.push(previous)
        return table


def enter(table, name, typename, offset):
    '''
    在table指向的符号表中为名字name建立新表项，同时将类型type及相对地址offset放入该表项的属性域中。
    '''
    item = stitem(name, typename, offset)
    table.push(item)


def addwidth(table, width):
    '''
    将table指向的符号表中所有表项的宽度之和记录在与符号表关联的表头中。
    '''
    table.width = width


def enterproc(table, name, newtable):
    '''
    在table指向的符号表中为过程name建立一个新表项，参数newtable指向过程name的符号表。
    '''
    table[name] = newtable
    return table


class sa:
    tblptrStack = []  # 保存指向外围过程符号表的指针。
    offsetStack = []  # 其栈顶元素是下一个当前过程中局部对象可用的相对地址。

    def __init__(self, strItemList):
        self.strItemList = strItemList

    def P(self):
        self.M()
        self.D()
        addwidth(self.tblptrStack[-1], self.offsetStack[-1])
        popoffset = self.offsetStack.pop()
        poptable = self.tblptrStack.pop()
        return poptable

    def M(self):
        table = tbl()
        self.tblptrStack.append(table)
        self.offsetStack.append(0)

    def D(self):
        if self.strItemList[-1].state != 0:
            if self.strItemList[-1].state == 1:
                strItem = self.strItemList.pop()
                if self.strItemList[-1].state == 2:
                    strItem2 = self.strItemList.pop()
                    Temp = self.T()
                    typename = Temp['type']
                    width = Temp['width']
                    self.offsetStack[-1] += width
                    enter(self.tblptrStack[-1], strItem.strname,
                          typename, self.offsetStack[-1])
                    self.tblptrStack[-1].width = self.offsetStack[-1]
                    self.D2()

    def D2(self):
        if self.strItemList[-1].state == 3:
            self.strItemList.pop()
            self.D()
            self.D2()

    def T(self):
        Temp = {}
        strItem = self.strItemList.pop()
        if strItem.strname == 'integer':
            Temp['type'] = strItem.strname
            Temp['width'] = 4
        elif strItem.strname == 'real':
            Temp['type'] = strItem.strname
            Temp['width'] = 8
        elif strItem.strname == 'ptr':
            Temp['type'] = strItem.strname + ' ' + self.T()['type']
            Temp['width'] = 4
        else:
            print('ERROR: The key word not found')
        return Temp


strs = 'id1:real;id2:ptr integer;id3:integer;'
strs += '#'
lexer = lexer(strs)
lexer.convert()
stritemList = lexer.getstritemList()
sa = sa(stritemList[::-1])
table = sa.P()
print('name'+' '+'type'+'         '+'offset')
for v in table.tbl.values():
    print("%-5s%-13s%-10d"%(v.name,v.typename,v.offset))
