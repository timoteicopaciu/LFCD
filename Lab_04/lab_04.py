from texttable import Texttable


class TableFA:
    """
    This class represent a FA as a table
    """
    def __init__(self):
        self.__initialState = ''
        self.__finalStates = []
        self.__alphabet = {}
        self.__states = {}
        self.__transitionTable = []
        self.__isDFA = True

    def readFAFromFile(self, filename):
        """
        Read a FA from a file
        :param filename: string, the name of the name where FA is stored
        :preconditions: filename must to be a string, representing a file name
        :postconditions: the FA object's attributes will be completed
        :return: none
        """
        fin = open(filename, 'r')
        # read initial state
        line = fin.readline()
        self.__initialState = line.strip('\n')
        # read final states
        line = fin.readline()
        line = line.strip('\n')
        self.__finalStates = line.split(',')
        # read alphabet
        line = fin.readline()
        line = line.strip('\n')
        alphabet = line.split(',')
        for i in range(1, len(alphabet) + 1):
            self.__alphabet[alphabet[i - 1]] = i
        # read states
        line = fin.readline()
        line = line.strip('\n')
        states = line.split(',')
        for i in range(1, len(states) + 1):
            self.__states[states[i - 1]] = i
        # build transition table
        self.__transitionTable.append([''] + list(self.__alphabet.keys()))
        for state in list(self.__states.keys()):
            self.__transitionTable.append([state])
            l = []
            for letter in list(self.__alphabet.keys()):
                line = fin.readline()
                line = line.strip('\n')
                endStates = line.split(',')
                l = l + endStates
                self.__transitionTable[self.__states[state]].append(endStates)

            l = list(filter(('-').__ne__, l))
            if len(l) > len(set(l)):
                print('Is not a DFA!')
                self.__isDFA = False


    def print(self, x):
        """
        Print some attributes of FA
        :param x: char, representing an option in order to know what to return
        :preconditions: x must be a string, x is from A = {'1', '2', '3', '4'}
        :postconditions: a string is returned, representing an attribute as a string, or '' if x is not in A
        :return: a string
        """
        if x == '1':
            return str(list(self.__states.keys()))
        elif x == '2':
            return str(list(self.__alphabet.keys()))
        elif x == '3':
            t = Texttable()
            for lst in self.__transitionTable:
                t.add_row(lst)
            return t.draw()
        elif x == '4':
            return str(self.__finalStates)
        return ''

    def isAccepted(self, sequence):
        """
        Verify if a sequence is accepted by the FA
        :param sequence: string, the sequence to be verified if is accepted by he FA
        :preconditions: sequence must to be a string
        :postconditions: return if the sequence is accepted or not
        :return: 'Is accepted!' or 'Is not accepted!' or 'Is not a DFA!'
        """
        if self.__isDFA == False:
            return 'Is not a DFA!'
        if len(sequence) == 0 and self.__initialState in self.__finalStates:
            return 'Is accepted!'
        # if sequence[0] not in self.__initialState or sequence[-1] not in self.__finalStates:
        #     return 'Is not accepted!'
        state = self.__initialState
        for x in sequence:
            if x not in self.__alphabet:
                return 'Is not accepted!'
            state = self.__transitionTable[self.__states[state]][self.__alphabet[x]][0]
            if state == '-':
                return 'Is not accepted!'

        if state not in self.__finalStates:
            return 'Is not accepted!'
        return 'Is accepted!'




if __name__ == '__main__':
    FA = TableFA()
    FA.readFAFromFile('FA.in')
    while 1:
        print('Choose a number:')
        print('\t0.Exit')
        print('\t1.Print the set of states')
        print('\t2.Print the alphabet')
        print('\t3.Print all the transitions')
        print('\t4.Print the set of final states')
        print('\t5.Verify if a sequence is accepted by the FA')
        x = input()
        if x == '0':
            break
        elif x == '5':
            seq = input('Give the sequence:')
            print(FA.isAccepted(seq))
        else:
            print(FA.print(x))
