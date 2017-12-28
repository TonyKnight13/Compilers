'''
词法分析器
'''


class DFA:
    file_object = ''
    resWord = {'begin': '1', 'if': '2', 'then': '3',
               'while': '4', 'do': '5', 'end': '6'}  # 关键字
    state = 0  # 种别码
    lineNum = 0  # 行數
    charMessage = []

    def __init__(self, file_name):
        self.file_object = file_name
        self.state = -1
        self.lineNum = 0
        self.errorMessage = []
        self.charMessage = []

    def Convert(self):
        for line in self.file_object:
            line = line.strip('\n')
            self.lineNum += 1
            lineLength = len(line)
            i = 0
            string = ''
            while i < lineLength:
                ch = line[i]
                i += 1
                if self.state == -1:
                    if ch.isalpha():
                        self.state = 10
                        string = ch
                    elif ch.isspace():
                        self.state = -1
                    elif ch.isdigit():
                        self.state = 11
                        string = ch
                    elif ch == '+':
                        self.state = 13
                        content = '(' + str(self.state) + ',+)'
                        self.charMessage.append(content)
                        self.state = -1
                    elif ch == '-':
                        self.state = 14
                        content = '(' + str(self.state) + ',-)'
                        self.charMessage.append(content)
                        self.state = -1
                    elif ch == '*':
                        self.state = 15
                        content = '(' + str(self.state) + ',*)'
                        self.charMessage.append(content)
                        self.state = -1
                    elif ch == '/':
                        self.state = 16
                        content = '(' + str(self.state) + ',/)'
                        self.charMessage.append(content)
                        self.state = -1
                    elif ch == ':':
                        self.state = 17
                    elif ch == '<':
                        self.state = 20
                    elif ch == '>':
                        self.state = 23
                    elif ch == '=':
                        self.state = 25
                        content = '(' + str(self.state) + ',=)'
                        self.charMessage.append(content)
                        self.state = -1
                    elif ch == ';':
                        self.state = 26
                        content = '(' + str(self.state) + ',;)'
                        self.charMessage.append(content)
                        self.state = -1
                    elif ch == '(':
                        self.state = 27
                        content = '(' + str(self.state) + ',()'
                        self.charMessage.append(content)
                        self.state = -1
                    elif ch == ')':
                        self.state = 28
                        content = '(' + str(self.state) + ',))'
                        self.charMessage.append(content)
                        self.state = -1
                    elif ch == '#':
                        self.state = 0
                        content = '(' + str(self.state) + ',#)'
                        self.charMessage.append(content)
                        self.state = -1
                    else:
                        content = 'ERROR:行号为' + \
                            str(self.lineNum) + ',' + ch + '字符不可识别'
                        self.charMessage.append(content)
                        self.state = -1
                elif self.state == 10:
                    if ch.isalpha():
                        string += ch
                        self.state = 10
                    elif ch.isdigit():
                        string += ch
                        self.state = 10
                    else:
                        if string in self.resWord.keys():
                            self.state = self.resWord.get(string)
                        content = '(' + str(self.state) + ',' + string + ')'
                        self.charMessage.append(content)
                        string = ''
                        self.state = -1
                        i -= 1
                elif self.state == 11:
                    if ch.isdigit():
                        string += ch
                        self.state = 11
                    elif ch.isalpha():
                        content = 'ERROR:行号为' + str(self.lineNum) + ',' + ch
                        self.charMessage.append(content)
                        string = ''
                        self.state = -1
                    else:
                        if (string[0] == '0' and len(string) > 1):
                            content = 'ERROR:行号为' + \
                                str(self.lineNum) + ',' + string + '的首位为零'
                            self.charMessage.append(content)
                            string = ''
                            self.state = -1
                            i -= 1
                        else:
                            content = '(' + str(self.state) + \
                                ',' + string + ')'
                            self.charMessage.append(content)
                            string = ''
                            self.state = -1
                            i -= 1
                elif self.state == 17:
                    if ch == '=':
                        self.state = 18
                        content = '(' + str(self.state) + ',:=)'
                        self.charMessage.append(content)
                        self.state = -1
                    else:
                        content = '(' + str(self.state) + ',:)'
                        self.charMessage.append(content)
                        self.state = -1
                        i -= 1
                elif self.state == 20:
                    if ch == '>':
                        self.state = 21
                        content = '(' + str(self.state) + ',<>)'
                        self.charMessage.append(content)
                        self.state = -1
                    elif ch == '=':
                        self.state = 22
                        content = '(' + str(self.state) + ',<=)'
                        self.charMessage.append(content)
                        self.state = -1
                    else:
                        content = '(' + str(self.state) + ',<)'
                        self.charMessage.append(content)
                        self.state = -1
                        i -= 1
                elif self.state == 23:
                    if ch == '=':
                        self.state = 24
                        content = '(' + str(self.state) + ',>=)'
                        self.charMessage.append(content)
                        self.state = -1
                    else:
                        content = '(' + str(self.state) + ',>)'
                        self.charMessage.append(content)
                        self.state = -1
                        i -= 1

    def getChar(self):  # 获取识别信息
        return self.charMessage

    def getError(self):  # 获取错误信息
        return self.errorMessage


fileobject = open("C:\\Users\\Administrator\\Desktop\\test.txt")
dfa = DFA(fileobject)
dfa.Convert()
content = dfa.getChar()
for item in content:
    print(item)

fileobject.close()
