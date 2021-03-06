
class Grammar:
    def __init__(self):
        self.__nonTerminals = []
        self.__terminals = []
        self.__startSymbol = None
        self.__productions = {}
        self.__word = ''

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
        self.__terminals = line.split(' ')
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
        inputStack = self.__productions[headOfInputStack][0].split(' ') + inputStack[1:]
        # inputStack[0] = self.__productions[headOfInputStack][0] #get first production

        assert workingStackLen + 1 == len(workingStack)
        # assert inputStackLen == len(inputStack)

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

        assert workingStackLen + 1 == len(workingStack)
        assert inputStackLen -1 == len(inputStack)

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

        assert workingStackLen - 1 == len(workingStack)
        assert inputStackLen + 1 == len(inputStack)

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
        j = int(j)
        if j + 1 < len(self.__productions[headOfWorkingStack]):
            j += 1
            workingStack[-1] = str(headOfWorkingStack) + '_' + str(j)
            len_prev = len(self.__productions[headOfWorkingStack][j - 1].split(' '))
            inputStack = self.__productions[headOfWorkingStack][j].split(' ') +  inputStack[len_prev:] # get production j

            assert workingStackLen == len(workingStack)
            # assert inputStackLen == len(inputStack)

            return 'q', index, workingStack, inputStack
        elif index == 0 and headOfWorkingStack == self.__startSymbol:
            return 'e', index, workingStack, inputStack
        else:
            len_prev = len(self.__productions[headOfWorkingStack][j].split(' '))
            inputStack = [headOfWorkingStack] + inputStack[len_prev:]
            workingStack = workingStack[:-1]

            assert workingStackLen - 1 == len(workingStack)
            # assert inputStackLen == len(inputStack)

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

    def setWord(self,word):
        self.__word = word

    def getStartSymbol(self):
        return self.__startSymbol

    def parse(self, state, index, workingStack, inputStack, out, maxIndex):
        """
         This function parse the word set in self.__word item and check if is a accepted sequence using recursion
         :param state: a char
             :pre: 'q'
             :post: any state
         :param index: integer
             :pre: 0
             :post: some integer
         :param workingStack: a list, representing the working stack, stores the way the parse is built
             :pre: []
             :post: same list W
         :param inputStack: a list, representing  input stack, part of the tree to be built
             :pre: a list containing just starting symbol
             :post: empty list
         :param out: a file descriptor to the file where the track of operations to be printed
             :pre: a file descriptor
             :post: same file descriptor
         :param maxIndex: a number, integer, representing an index in word, the best parse matches all untill that index in word
         :return: a ParserOutput object
         """
        if state == 'f':
            return self.buildParserOutput(workingStack), maxIndex

        elif state == 'e':
            return ParserOutput(['Error!']), maxIndex

        elif state == 'q' and index == len(word) and len(inputStack) == 0:
            state, index, workingStack, inputStack = self.success(state, index, workingStack, inputStack)
            out.write('Success ' + str(state) + ', ' + str(index) + ', ' + str(workingStack) + ', ' + str(inputStack) + ', maxIndex=' + str(maxIndex) + '\n')
            return self.parse(state, index, workingStack, inputStack, out, max(index, maxIndex))

        elif state == 'q' and len(inputStack) != 0 and inputStack[0] in self.__nonTerminals:
            state,index,workingStack,inputStack = self.expand(state, index, workingStack, inputStack)
            out.write('Expand ' + str(state) + ', ' + str(index) + ', ' + str(workingStack) + ', ' + str(inputStack) + ', maxIndex=' + str(maxIndex) + '\n')
            return self.parse(state, index, workingStack, inputStack, out, max(index, maxIndex))

        elif state == 'q' and len(inputStack) != 0 and inputStack[0] in self.__terminals and index < len(self.__word) and inputStack[0] == self.__word[index]:
            state, index, workingStack, inputStack = self.advance(state, index, workingStack, inputStack)
            out.write('Advance ' + str(state) + ', ' + str(index) + ', ' + str(workingStack) + ', ' + str(inputStack) + ', maxIndex=' + str(maxIndex) + '\n')
            return self.parse(state, index, workingStack, inputStack, out, max(index, maxIndex))

        elif state == 'q' and (len(inputStack) == 0 or (inputStack[0] in self.__terminals and (index >= len(self.__word) or inputStack[0] != self.__word[index]))):
            state, index, workingStack, inputStack = self.momentaryInsuccess(state, index, workingStack, inputStack)
            out.write(
                'Momentary Insuccess ' + str(state) + ', ' + str(index) + ', ' + str(workingStack) + ', ' + str(inputStack) + ', maxIndex=' + str(maxIndex) + '\n')
            return self.parse(state, index, workingStack, inputStack, out, max(index, maxIndex))

        elif state == 'b' and workingStack[-1] in self.__terminals:
            state, index, workingStack, inputStack = self.back(state, index, workingStack, inputStack)
            out.write(
                'Back ' + str(state) + ', ' + str(index) + ', ' + str(workingStack) + ', ' + str(inputStack) + ', maxIndex=' + str(maxIndex) + '\n')
            return self.parse(state, index, workingStack, inputStack, out, max(index, maxIndex))

        elif state == 'b' and '_' in workingStack[-1] and workingStack[-1].split('_')[0] in self.__nonTerminals:
            state, index, workingStack, inputStack = self.anotherTry(state, index, workingStack, inputStack)
            out.write(
                'Another Try ' + str(state) + ', ' + str(index) + ', ' + str(workingStack) + ', ' + str(inputStack) + ', maxIndex=' + str(maxIndex) + '\n')
            return self.parse(state, index, workingStack, inputStack, out, max(index, maxIndex))

        else:
            state = 'e'
            return self.parse(state, index, workingStack, inputStack, out, max(index, maxIndex))

    def buildParserOutput(self, workingStack):
        """
        This function make an object of type ParserOutput from the working stack given as result of parser
        :param workingStack: a list, the working stack given as result from parser
        :return: an object of type ParserOutput
        """
        derivationsString = [[self.__startSymbol]]
        for x in workingStack:
            if '_' in x:
                non_terminal, productionIndex = x.split('_')
                productionIndex = int(productionIndex)
                lastDerivation = derivationsString[-1]
                index = lastDerivation.index(non_terminal)
                derivationsString.append(lastDerivation[:index] + self.__productions[non_terminal][productionIndex].split(' ') + lastDerivation[index + 1:])

        return ParserOutput(derivationsString)

class ParserOutput:
    """
    Represent the output of a parser as a derivations string
    """
    def __init__(self, derivationString):
        self.__derivationString = derivationString

    def toString(self):
        """
        Represent the parser output object as a string
        :return: a string, representing the parser output object as a string
        """
        out = ''
        nrOfCurrentDerivationString = 0
        derivationStringLen = len(self.__derivationString)
        for ds in self.__derivationString:
            nrOfCurrentDerivationString += 1
            for el in ds:
                out = out + str(el) + " "
            if nrOfCurrentDerivationString < derivationStringLen:
                out = out + "=> "
        return out

    def printToConsole(self):
        """
        Print to the console the out of the parser as a derivations string
        :return: None
        """
        if self.__derivationString == ['Error!']:
            print(self.toString())
        else:
            print('The derivations string is:\n' + self.toString())

    def printToFile(self, file):
        """
        Print to the file the out of the parser as a derivations string
        :param file: a file descriptor, representing the file where to write
        :return: None
        """

        if self.__derivationString == ['Error!']:
            file.write(self.toString())
        else:
            file.write('The derivations string is:\n' + self.toString())



if __name__ == '__main__':
    g1 = Grammar()
    g1.readGrammar('g1.txt')

    g2 = Grammar()
    g2.readGrammar('g2.txt')
    while 1:
        print('Choose a number:')
        print('\t0.Exit')
        print('\t1.Print the set of non-terminal symbols for grammar from g1.txt')
        print('\t2.Print the set of terminal symbols for grammar from g1.txt')
        print('\t3.Print the set of productions for grammar from g1.txt')
        print('\t4.Print the set of final states for a non terminal for grammar from g1.txt')
        print('\t5.Parse word from seq.txt with grammar from g1.txt')
        print('\t6.Print the set of non-terminal symbols for grammar from g2.txt')
        print('\t7.Print the set of terminal symbols for grammar from g2.txt')
        print('\t8.Print the set of productions for grammar from g2.txt')
        print('\t9.Print the set of final states for a non terminal for grammar from g2.txt')
        print('\t10.Parse word from PIF.out with grammar from g2.txt')
        x = input()
        if x == '0':
            break
        elif x == '4':
            non_terminal = input('Give the non-terminal:')
            print(g1.print(x, non_terminal))
        elif x == '5':
            out1 = open('out1.txt', 'w')
            fin = open('seq.txt', 'r')
            out = open('track.out', 'w')
            word = fin.readline()
            word = word.split(' ')
            fin.close()
            out1.write('The word to be matched is:\n' + str(word) + '\n')
            g1.setWord(word)
            parserOutput, maxIndex = g1.parse('q', 0, [], [g1.getStartSymbol()], out, -1)
            out1.write("Max sequence that was matched is:\n" + str(word[:maxIndex]) + '\n')
            parserOutput.printToFile(out1)
            out1.close()
            out.close()
        elif x == '1' or x == '2' or x == '3':
            print(g1.print(x))
        elif x == '9':
            non_terminal = input('Give the non-terminal:')
            print(g2.print(x, non_terminal))
        elif x == '10':
            out2 = open('out2.txt', 'w')
            fin = open('PIF.out', 'r')
            word = []
            line = fin.readline()
            while len(line) != 0:
                word.append(line.split(' ')[0])
                line = fin.readline()
            out2.write('The word to be matched is:\n' + str(word) + '\n')
            fin.close()

            out = open('track.out', 'w')
            g2.setWord(word)
            parserOutput, maxIndex = g2.parse('q', 0, [], [g2.getStartSymbol()], out, -1)
            out2.write("Max sequence that was matched is:\n" + str(word[:maxIndex]) + '\n')
            parserOutput.printToFile(out2)
            out.close()
            out2.close()
        elif x == '6' or x == '7' or x == '8':
            print(g2.print(x))
        else:
            print('No such option!')