
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
        :param nonterminal: string, a nonterminal, production starting from it will be printed
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



if __name__ == '__main__':
    g = Grammar()
    g.readGrammar('g2.txt')
    while 1:
        print('Choose a number:')
        print('\t0.Exit')
        print('\t1.Print the set of nonterminal symbols')
        print('\t2.Print the set of terminal symbols')
        print('\t3.Print the set of productions')
        print('\t4.Print the set of final states for a non terminal')
        x = input()
        if x == '0':
            break
        elif x == '4':
            nonterminal = input('Give the nonterminal:')
            print(g.print(x, nonterminal))
        else:
            print(g.print(x))
