class FileIO:
    def __init__(self):
        self.boiler_plate = '''
            #include <stdio.h>
            #include <stdlib.h>

            int main(void){
                
            }
        '''.replace('    ', '')

        self.file = 'code.c'
        self.prev_code = self.boiler_plate
        #resetting/creating the file
        with open(self.file, 'w') as f: f.write(self.boiler_plate)

    def _reset_file_on_error(func):
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            
            except Exception as e:
                # print(e)
                # self = args[0]
                # with open(self.file, 'w') as f:
                #     f.write(self.boiler_plate)
                
                # return func(*args, **kwargs)
                pass

        return inner

    @_reset_file_on_error
    def _rewrite_into_main(self, new_code):
        substr = 'int main(void){'
        start = self.prev_code.index(substr) + len(substr)
        return self.prev_code[:start + 1] + new_code + '\n}'

    @_reset_file_on_error
    def _append_into_main(self, new_code):
        end_of_main = 0
        #gets last occurance of '}'
        for idx, char in enumerate(self.prev_code):
            if char == '}':
                end_of_main = idx

        return self.prev_code[:end_of_main] + new_code + '\n}'

    def delete_last_line(self):
        with open(self.file, 'r') as f:
            code = f.read()

        code = code.split('\n')
        #last line is closing curly bracket so we have to remove one before that
        code.pop(-2)
        code = '\n'.join(code)

        with open(self.file, 'w') as f:
            f.write(code)

    @_reset_file_on_error
    def write_code_to_file(self, code):
        with open(self.file, 'r') as f:
            self.prev_code = f.read()

        new_text = self._append_into_main(code)
        with open(self.file, 'w') as f:
            f.write(new_text)
