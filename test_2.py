from colorama import init
from prompt_toolkit import print_formatted_text
from prompt_toolkit.shortcuts import prompt
from pygments.lexers.c_cpp import CLexer
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles.pygments import style_from_pygments_cls
from pygments.styles import get_style_by_name
from prompt_toolkit.completion import WordCompleter


html_completer = WordCompleter(['printf', 'getchar'])
init()

myStyle = style_from_pygments_cls(get_style_by_name('C_REPL'))
init()

while True:
    prompt('>>> ', lexer = PygmentsLexer(CLexer), style = myStyle, include_default_pygments_style = True, completer = html_completer)

num = 5
