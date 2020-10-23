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
        return i

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
        return self.__binaryTree.addItem(value)

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




def scan(filename):
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
        tokens = re.split('(\[|\]|\{|\}|\(|\)|;|,| |\+|%|>>|/|<|<=|>|>=|==|!=|=)', line)
        for token in tokens:
            if token == '' or token == ' ':
                continue
            if token in reserved_words or token in operators or token in separators:
                PIF.append((token, -1))
            elif re.match('^[A-Za-z_]*$', token) != None or re.match('^[-0-9]*$', token) != None or re.match('^[A-Za-z_?!\"]*$', token) != None:
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

    ST.print()


scan("p1.txt")