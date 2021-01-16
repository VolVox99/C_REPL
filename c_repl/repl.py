import sys
from c_repl.executer import Executer

class Repl:
    def __init__(self):
        self.executer = Executer()
        self.command_start = '/'
        self._commands = {
            #|| -> both keys map to same value
            'quit || exit': lambda: sys.exit(),
            'reset': lambda: self.executer.reset(),
            'undo': lambda: self.executer.fileIO.file_empty() or self.executer.fileIO.delete_last_line(),
            'abort': lambda: 0,
            'help': lambda: self.help_command(),
        }

        self._regular_start = '>>>'
        self._multiline_start = '...'
        self.indent = '\t'
        self.title = 'C REPL'
        self.set_title()

    @property
    def multiline_start(self):
        return self._multiline_start + ' '

    @property
    def regular_start(self):
        return self._regular_start + ' '
    
    @property
    def commands(self):
        return {self.command_start + key.strip():v for k, v in self._commands.items() for key in k.split('||')}

    @staticmethod
    def condense(code):
        return code.strip().replace('\n', ' ')

    @staticmethod
    def print_start(start):
        print(start, end = '')

    @staticmethod
    def check_end_of_line(code_section, total_code):
        return not code_section or (code_section.endswith('}') or code_section.endswith('};')) and total_code.count('{') == total_code.count('}')

    @staticmethod
    def help_command():
        pass

    def set_title(self):
        self.executer.run_command(f'title {self.title}')

    def execute_command(self, command :str, *args, **kwargs):
        return self.commands[command](*args, **kwargs)

    def check_for_command(self, code):
        for command in self.commands:
            if code == command:
                return self.execute_command(command) or True

        #check for invalid command
        if code.startswith(self.command_start):
            print("Invalid REPL command")
            return True

        return False
    
    def execute_code(self, code):
        print(self.executer.interpret(code))

    def get_input(self):
        try:
            return input()

        except (KeyboardInterrupt, EOFError):
            self.execute_command('/quit')

    def check_multiline(self, code, indent_level = 1):

        if code.endswith('{') or (not code.endswith(';') and not code.endswith('}') and not code.startswith('#')):
            while True:
                total_indent_level = self.indent * (indent_level + code.count('   ') + code.count(self.indent) )
                self.print_start(self.multiline_start + total_indent_level)
                new_code = self.get_input()
                if new_code.endswith('}'): 
                    indent_level -= 1

                code += new_code
                if self.check_end_of_line(new_code, code):
                    break

                elif self.check_for_command(new_code):
                    return ''
                
                #recursion to account for nested, ie for loop in function
                code = self.check_multiline(self.condense(code), indent_level + 1)

        return self.condense(code)

    #checks if user enters in string, to print it
    @staticmethod
    def check_print(code):
        if code.startswith('"') and code.endswith(';'):
            return "printf(" + code[:-1] + ");putchar('\n');"
        
        return code


    def run(self):
        while True:
            self.print_start(self.regular_start)
            code = self.condense(self.get_input())
            if not self.check_for_command(code):
                if not code: continue
                code = self.check_print(code)
                code = self.check_multiline(code)
                self.execute_code(code)
                self.executer.cleanup(code)