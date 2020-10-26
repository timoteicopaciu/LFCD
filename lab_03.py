import re

from importlib.machinery import SourceFileLoader

foo = SourceFileLoader("module.name", "D:\Faculty\Year_III_Sem_I\LFCD\Lab 2\lab_02.py").load_module()

def scan(filename):
    """
    Scan a program
    :param filename: string, the name of the file to be scanned
    :return: none
    """
    f = open(filename, "r")
    line = f.readline()
    lineNo = 1

    ST = foo.SymbolTable()
    operators = ['+', '-', '/', '%', '<', '<=', '>', '>=', '==', '!=', '=', '*', '>>']
    separators = [',', ';', '{', '}', '(', ')', '[', ']']
    reserved_words = ['main', 'define', 'Integer', 'Char', 'while', 'for', 'if', 'else', 'out', 'String', 'in.Integer', 'in.Chars']

    PIF = []
    while len(line) != 0:
        line = line.strip()
        tokens = re.split('(\[|\]|\{|\}|\(|\)|;|,|\s|\+|-|\*|/|%|>>|<=|>=|==|!=|=|<|>)', line)
        for token in tokens:
            if token == '' or token == ' ':
                continue
            if token in reserved_words or token in operators or token in separators:
                PIF.append((token, -1))
            elif re.match('^[A-Za-z][A-Za-z_]*$', token) != None or re.match('^[-]{0,1}[1-9]{1}[0-9]*$', token) != None or token == '0' or re.match('^\'[A-Za-z]{1}[A-Za-z_?!]*\'$', token) != None:
                if ST.findID(token) == -1:
                    id = ST.add(token)
                else:
                    id = ST.findID(token)
                PIF.append(('ID', id))
            else:
                print('Error at line ' + str(lineNo) + " with token " + token)

        line = f.readline()
        lineNo += 1

    fout = open("PIF.out", "w")
    for x in PIF:
        fout.write(str(x[0] + " -> " + str(x[1]) + "\n"))
    fout.close()

    fout = open("ST.out", "w")
    fout.write("The ST is represented as a binary search tree\n")
    fout.write(ST.getString())
    fout.close()


scan("perr.txt")
