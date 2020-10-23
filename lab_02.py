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
        return self.__binaryTree.getString()

ST = SymbolTable()
ST.add('ab')
ST.add('aa')
ST.add('ac')
ST.add('cd')
ST.add('124')
ST.add('123')

def euclideanAlgorithm(a, b):
    while a != b:
        if a > b:
            a = a - b
        else:
            b = b - a
    return a

"""
The purpose of this program is to give three different implementations for computing the Greatest Common Divisor of two numbers.
For each implementation I prepared an appropriate example in order to demonstrate how the program work. Also, I prepare some proofs and explinations for each implementation. 


"""
