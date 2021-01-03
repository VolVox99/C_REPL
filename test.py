from re import findall


code = 'printf("hello world"):'
is_func_defintion = findall('^\s*(?:(?:inline|static)\s+){0,2}(?!else|typedef|return)\w+\s+\*?\s*(\w+)\s*\([^0]+\)\s*;?', code)

print(is_func_defintion)