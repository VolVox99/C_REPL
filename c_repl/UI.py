import sys
from c_repl.executer import Executer

class Repl:
    def __init__(self):
        self.executer = Executer()
        self.exit_msg = 'quit'
        self.reset_msg = 'reset'

    @staticmethod
    def clean(code):
        return code.strip().replace('\n', ' ')

    def run(self):
        while True:
            print('>>> ', end = '')
            code = input()
            if code == self.exit_msg: sys.exit()
            elif code == self.reset_msg: self.executer.reset()
            elif code: 
                code = self.clean(code)
                result = self.executer.interpret(code)
                print(result)
                self.executer.cleanup(code)