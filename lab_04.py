import re

class BinarySearchTree:
    """
    Class BinarySearchTree represent a binary search tree and is represented on an array of numbers
    """
    def __init__(self, size):
        self.__tree = [''] * size
        self.__nrItems = 0

    def addItem(self, item):
        """
        Add a new item in the binary search tree
        :preconditions: item must be a string
        :postconditions: the item was added to ST if it wasn't added  yet
        :param item: item is a string
        :return: none
        """
        i = 1
        while self.__tree[i] != '':
            if self.__tree[i] == item:
                return
            if item < self.__tree[i]:
                i = i * 2
            else:
                i = i * 2 + 1
        self.__tree[i] = item
        self.__nrItems += 1

    def searchItemPosition(self, item):
        """
        Search position of a given item
        :preconditions: item must be a string
        :postconditions: the returned value is a number
        :param item: a string, representing the value to be searched
        :return: the position corresponding to the given item(value) in the BST, or -1 if is not present
        """
        i = 1
        while self.__tree[i] != '':
            if self.__tree[i] == item:
                return i
            if item < self.__tree[i]:
                i = i * 2
            else:
                i = i * 2 + 1
        return -1

    def size(self):
        """
        Give the size(in number of elements) of the binary search tree
        :preconditions: -
        :postconditions: -
        :return: integer, representing numbers of elements in the binary search tree
        """
        return self.__nrItems

    def printInorder(self, index):
        """
        Print the binary search tree in the Inorder Traversal
        :preconditions: index must be a number
        :postconditions: -
        :param index: the position in the array of the node
        :return: none
        """
        if self.__tree[index] != '':
            # Go to the left child
            self.printInorder(index * 2)
            # print root
            print((index, self.__tree[index])),
            # Go to the right child
            self.printInorder(index * 2 + 1)

    def getString(self):
        """
        Get BST as a string
        :preconditions: -
        :postconditions: -
        :return: BST as a string
        """
        out = ""
        i = 0
        for x in self.__tree:
            if x != '':
                out = out + str(i) + ": " + str(self.__tree[i]) + "\n"
            i += 1
        return out


class SymbolTable:
    def __init__(self):
        self.__binaryTree = BinarySearchTree(10000)

    def add(self, value):
        """
        Add a value to symbol table, if the value was not added yet
        :preconditions: value must be a string
        :postconditions: the value was added to ST if it wasn't added  yet
        :param value: a string, representing the value to be added in the ST
        :return: none
        """
        self.__binaryTree.addItem(value)

    def findID(self, value):
        """
        Give the position in BST(ID) of the corresponding value, or -1 if is not in ST
        :preconditions: value must be a string
        :postconditions: -
        :param value: a string, representing the value to be searched in the ST
        :return: an integer, representing the ID of the value, or -1 if the value ins't in ST
        """
        return self.__binaryTree.searchItemPosition(value)

    def print(self):
        """
        Print the ST
        :preconditions: -
        :postconditions: -
        :return:
        """
        self.__binaryTree.printInorder(1)

    def getString(self):
        """
        Return ST as a string
        :preconditions: -
        :postconditions: -
        :return: a string, representing ST
        """
        return self.__binaryTree.getString()

def scan(filename):
    """
    Scan a program
    :param filename: string, the name of the file to be scanned
    :preconditions: filename must to be a string, representing a file name
    :postconditions: the PIF and ST are printed in PIF.out, respectively ST.out, and if there are some errors they are printed on the console
    :return: none
    """
    f = open(filename, "r")
    line = f.readline()
    lineNo = 1

    ST = SymbolTable()
    operators = ['+', '-', '/', '%', '<', '<=', '>', '>=', '==', '!=', '=', '*', '>>']
    separators = [',', ';', '{', '}', '(', ')', '[', ']']
    reserved_words = ['main', 'define', 'Integer', 'Char', 'while', 'for', 'if', 'else', 'out', 'String', 'in.Integer', 'in.Chars']

    PIF = []
    while len(line) != 0:
        line = line.strip()
        tokens = re.split('(\[|\]|\{|\}|\(|\)|;|,|\s|\+|-|\*|/|%|>>|<=|>=|==|!=|=|<|>)', line)
        for i in range(len(tokens)):
            token = tokens[i]
            if token == '' or token == ' ':
                continue
            if token in reserved_words or token in operators or token in separators:
                if (tokens[i] == '-' or tokens[i] == '+') and re.match('^[-]{0,1}[1-9]{1}[0-9]*$', tokens[i - 1]) == None and tokens[i - 1] != '0' and (re.match('^[1-9]{1}[0-9]*$', tokens[i + 1]) != None or tokens[i + 1] == '0'):
                    tokens[i + 1] = tokens[i] + tokens[i+1]
                    continue
                PIF.append((token, -1))
            elif re.match('^[A-Za-z][A-Za-z_]*$', token) != None:
                if ST.findID(token) == -1:
                    ST.add(token)
                id = ST.findID(token)
                PIF.append(('ID', id))
            elif re.match('^[-]{0,1}[1-9]{1}[0-9]*$', token) != None or token == '0' or re.match('^\'[A-Za-z]{1}[A-Za-z_?!]*\'$', token) != None:
                if ST.findID(token) == -1:
                    ST.add(token)
                id = ST.findID(token)
                PIF.append(('CONST', id))
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


scan("p2.txt")