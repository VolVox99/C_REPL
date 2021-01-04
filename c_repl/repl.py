import sys
from c_repl.executer import Executer

class Repl:
    def __init__(self):
        self.executer = Executer()
        self.command_start = '/'
        self._commands = {
            'quit': lambda: sys.exit(),
            'reset': lambda: self.executer.reset(),
        }

    @staticmethod
    def clean(code):
        return code.strip().replace('\n', ' ')
    
    @property
    def commands(self):
        return {self.command_start + k: v for k, v in self._commands.items()}

    def execute_command(self, command, *args, **kwargs):
        return self.commands[command](*args, **kwargs)

    def check_for_command(self, code):
        for command in self.commands:
            if code == command:
                return self.execute_command(command) or True
                
        return False


    def run(self):
        while True:
            print('>>> ', end = '')
            code = input()
            if not self.check_for_command(code): 
                code = self.clean(code)
                result = self.executer.interpret(code)
                print(result)
                self.executer.cleanup(code)