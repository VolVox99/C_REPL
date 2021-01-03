from c_repl.fileIO import FileIO
from subprocess import check_output, CalledProcessError
from sys import exit
from re import findall


class Executer:
    def __init__(self):
        self.fileIO = FileIO()
        self.output_file = 'output'
        self.remove_funcs = ['printf', 'fprintf(stdout', 'getchar', 'putchar', 'scanf', 'fscanf(stdin', 'puts', 'gets', 'fgets(stdin', 'fputs(stdout']

    @staticmethod
    def run_command(command):
        return check_output(command).decode()

    def interpret(self, code):
        self.fileIO.write_code_to_file(code)
        try:
            self.run_command(f'gcc {self.fileIO.file} -o {self.output_file}')

        except CalledProcessError:
            self.fileIO.delete_last_line()
            self.run_command(f'gcc {self.fileIO.file} -o {self.output_file}')

        except FileNotFoundError:
            print("GCC must be installed to use c_repl\nYou can install it here: https://gcc.gnu.org/install/")
            exit(1)

        return self.run_command(f'./{self.output_file}')

    def reset(self):
        self.__init__()

    def cleanup(self, code):
        #regex for function prototypes
        func_defintion = findall('^\s*(?:(?:inline|static)\s+){0,2}(?!else|typedef|return)\w+\s+\*?\s*(\w+)\s*\([^0]+\)\s*;?', code)
        if func_defintion: 
            for definition in func_defintion:
                self.remove_funcs.append(definition)
            return

        for func in self.remove_funcs:
            if func in code:
                self.fileIO.delete_last_line()
                return 
        