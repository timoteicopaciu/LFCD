
class Grammar:
    def __init__(self):
        self.__nonTerminals = []
        self.__terminals = []
        self.__startSymbol = None
        self.__productions = {}

    def readGrammar(self, filename):
        """
        Read a Grammar from a file
        :param filename: string, the name of the name where Grammar is stored
        :preconditions: filename must to be a string, representing a file name
        :postconditions: the Grammar object's attributes will be completed
        :return: none
        """
        fin = open(filename, 'r')
        line = fin.readline()
        line = line.strip(' \n')
        self.__nonTerminals = line.split(',')
        line = fin.readline()
        line = line.strip(' \n')
        self.__terminals = line.split(',')
        line = fin.readline()
        line = line.strip(' \n')
        self.__startSymbol = line
        line = fin.readline()
        while line != '':
            line = line.strip(' \n')
            x = line.split('->')
            self.__productions[x[0]] = []
            for y in x[1].split('|'):
                self.__productions[x[0]].append(y)
            line = fin.readline()

    def print(self, x, nonterminal = None):
        """
        Print some attributes of Grammar
        :param x: char, representing an option in order to know what to return
        :param nonterminal: string, a nonterminal, production starting from it will be printed, is optional
        :preconditions: x must be a string, x is from A = {'1', '2', '3', '4'}
        :postconditions: a string is returned, representing an attribute as a string, or '' if x is not in A
        :return: a string
        """
        if x == '1':
            return str(self.__nonTerminals)
        elif x == '2':
            return str(self.__terminals)
        elif x == '3':
            out = ''
            for x1 in self.__productions.keys():
                for x2 in self.__productions[x1]:
                   out = out + ' ' + x1 + ' -> ' + x2 + ';'
            return out
        elif x == '4':
            out = ''
            if nonterminal != None and nonterminal in self.__nonTerminals:
                for x2 in self.__productions[nonterminal]:
                    out = out + ' ' + nonterminal + ' -> ' + x2 + ';'
            return out
        return ''

    def expand(self, state, index, workingStack, inputStack):
        """
        Expand function
        :param state: a char
            :pre: 'q'
            :post: 'q'
        :param index: integer
            :pre: some integer i
            :post: same i
        :param workingStack: a list, representing the working stack, stores the way the parse is built
            :pre: some list W
            :post: list W U A_0, where A_0 is a name for first prod of non-terminal A
        :param inputStack: a list, representing  input stack, part of the tree to be built
            :pre: A U I, where A is a non-terminal and I is a list
            :post: first prod of A U I
        :return: a configuration, all input params but updated
        """
        assert state == 'q'
        assert inputStack[0] in self.__nonTerminals

        workingStackLen = len(workingStack)
        inputStackLen = len(inputStack)
        headOfInputStack = inputStack[0]
        workingStack.append(str(headOfInputStack) + '_0')
        inputStack[0] = self.__productions[headOfInputStack][0] #get first production

        assert workingStackLen == len(workingStack) + 1
        assert inputStackLen == len(inputStack)

        return state, index, workingStack, inputStack

    def advance(self, state, index, workingStack, inputStack):
        """
        Advance function
        :param state: a char
            :pre: 'q'
            :post: 'q'
        :param index: integer
            :pre: some integer i
            :post: i + 1
        :param workingStack: a list, representing the working stack, stores the way the parse is built
            :pre: some list W
            :post: list W U a, where a is the first terminal from the input stack
        :param inputStack: a list, representing  input stack, part of the tree to be built
            :pre: a U I, where a is a terminal, a terminal = current symbol from input, and I is a list
            :post: I
        :return: a configuration, all input params but updated
        """
        assert state == 'q'
        assert inputStack[0] in self.__terminals

        workingStackLen = len(workingStack)
        inputStackLen = len(inputStack)
        headOfInputStack = inputStack[0]
        inputStack = inputStack[1:]
        workingStack.append(headOfInputStack)

        assert workingStackLen == len(workingStack) + 1
        assert inputStackLen == len(inputStack) - 1

        return state, index + 1, workingStack, inputStack

    def momentaryInsuccess(self, state, index, workingStack, inputStack):
        """
        MomentaryInsuccess function
        :param state: a char
            :pre: 'q'
            :post: 'b' back/previous state
        :param index: integer
            :pre: some integer i
            :post: same i
        :param workingStack: a list, representing the working stack, stores the way the parse is built
            :pre: some list W
            :post: same W
        :param inputStack: a list, representing  input stack, part of the tree to be built
            :pre: a U I, where a is a terminal and I is a list, a is different from current symbol from input
            :post: same a U I
        :return: a configuration, all input params but updated
        """
        assert state == 'q'
        assert inputStack[0] in self.__terminals

        return 'b', index, workingStack, inputStack

    def back(self, state, index, workingStack, inputStack):
        """
       Back function
       :param state: a char
           :pre: 'b'
           :post: 'b'
       :param index: integer
           :pre: some integer i
           :post: i - 1
       :param workingStack: a list, representing the working stack, stores the way the parse is built
           :pre: some list W U a, where a is a terminal
           :post: list W, without terminal a
       :param inputStack: a list, representing  input stack, part of the tree to be built
           :pre: I
           :post: a U I, where a is a terminal and I is a list
       :return: a configuration, all input params but updated
       """
        assert state == 'b'
        assert workingStack[-1] in self.__terminals

        workingStackLen = len(workingStack)
        inputStackLen = len(inputStack)
        headOfWorkingStack = workingStack[-1]
        workingStack = workingStack[:-1]
        inputStack = [headOfWorkingStack] + inputStack

        assert workingStackLen == len(workingStack) - 1
        assert inputStackLen == len(inputStack) + 1

        return state, index - 1, workingStack, inputStack

    def anotherTry(self, state, index, workingStack, inputStack):
        """
       AntoherTry function
       :param state: a char
           :pre: 'b'
           :post: 'q' or 'b' or 'e'
       :param index: integer
           :pre: some integer i
           :post: same i
       :param workingStack: a list, representing the working stack, stores the way the parse is built
           :pre: list W U A_j, where A_j is a name for the j-th prod of non-terminal A
           :post: list W U A_j+1 or just W
       :param inputStack: a list, representing  input stack, part of the tree to be built
           :pre: j-th prod of A U I
           :post: j+1-th prod of A U I or A or just I
       :return: a configuration, all input params but updated
       """
        assert state == 'b'

        workingStackLen = len(workingStack)
        inputStackLen = len(inputStack)
        headOfWorkingStack, j = workingStack[-1].split('_')
        if j + 1 < len(self.__productions[headOfWorkingStack]):
            j += 1
            workingStack[-1] = str(headOfWorkingStack) + '_' + str(j)
            inputStack[0] = self.__productions[headOfWorkingStack][j]  # get production j

            assert workingStackLen == len(workingStack)
            assert inputStackLen == len(inputStack)

            return 'q', index, workingStack, inputStack
        elif index == 1 and headOfWorkingStack == self.__startSymbol:
            return 'e', index, workingStack, inputStack
        else:
            inputStack[0] = headOfWorkingStack
            workingStack = workingStack[:-1]

            assert workingStackLen == len(workingStack) - 1
            assert inputStackLen == len(inputStack)

            return 'b', index, workingStack, inputStack

    def success(self, state, index, workingStack, inputStack):
        """
       Success function
       :param state: a char
           :pre: 'q'
           :post: 'f'
       :param index: integer
           :pre: some integer (n + 1)
           :post: same integer (n + 1)
       :param workingStack: a list, representing the working stack, stores the way the parse is built
           :pre: some list W
           :post: same list W
       :param inputStack: a list, representing  input stack, part of the tree to be built
           :pre: empty list
           :post: empty list
       :return: a configuration, all input params but updated
       """
        assert state == 'q'
        assert len(inputStack) == 0

        return 'f', index, workingStack, inputStack


if __name__ == '__main__':
    g = Grammar()
    g.readGrammar('g1.txt')
    while 1:
        print('Choose a number:')
        print('\t0.Exit')
        print('\t1.Print the set of non-terminal symbols')
        print('\t2.Print the set of terminal symbols')
        print('\t3.Print the set of productions')
        print('\t4.Print the set of final states for a non terminal')
        x = input()
        if x == '0':
            break
        elif x == '4':
            non_terminal = input('Give the non-terminal:')
            print(g.print(x, non_terminal))
        else:
            print(g.print(x))