from grammars.tsm import TSM

class Parser(object):
    @classmethod
    def parse(filename):
        tree = TSM.parse(filename)
