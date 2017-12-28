import collections


class s:
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
    def __init__(self, name, typename, offset):
        self.name = name
        self.typename = typename
        self.offset = offset


class tbl:
    tbl = collections.OrderedDict()

    def __init__(self, width=None):
        self.width = width

    def pop(self):
        popitem = self.tbl.popitem()
        return popitem

    def push(self, item):
        self.tbl[item.name] = item


def mktable(previous):
    table = tbl()
    if previous.name == '':
        return table
    else:
        table.push(previous)
        return table


def enter(table, name, typename, offset):
    item = stitem(name, typename, offset)
    table.push(item)


def addwidth(table, width):
    table.width = width


def enterproc(table, name, newtable):
    table[name] = newtable
    return table


class sa:
    tblptrStack = []
    offsetStack = []

    def __init__(self, strItemList):
        self.strItemList = strItemList

    def P(self):
        self.M()
        self.D()
        addwidth(self.tblptrStack[-1], self.offsetStack[-1])
        popoffset = self.offsetStack.pop()
        poptable = self.tblptrStack.pop()
        return poptable, popoffset

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
table, offset = sa.P()
for v in table.tbl.values():
    print('name:' + v.name)
    print('type:' + v.typename)
    print('offset:' + str(v.offset))
print(offset)
