"""
Die verschiedenen Tags werden seperat behandelt:
+ Enable
+ Use
+ Database
+ Table
+ Custom
+ Build
+ Fill

+ Output
"""

from re import finditer, search

from src.table import TableBuilder
from src.errors import *
from src.utils import is_empty
END = -1
HEADER = r'(<)(\w+)(\@?)(\'[^\']*\'|\W?)(\b[a-zA-Z_][a-zA-Z0-9_]*\b|.*)>'
    
class Converter:
    def __init__(self, filepath: str):
        with open(filepath) as file:
            self.data = file.read()
        self.headers = []
        self.contents = []
        self.ctx = ''
        
        
        self.current_tag = None
        self.current_content = None
        self.ident_char_tag = None
        self.ident_char_content = None
        
        
        self.SETTING_CREATE_DOCSTRINGS = False
        self.SETTING_CREATE_ACCESSOR = False
        self.SETTING_SCRIPT_INJECTION_ALLOWED = False
        self.SETTING_USAGE_ALLOWED = False
        self.__main_parser()
        try:
            self.__main_parser()
        except Exception as E:
            print(f"""
\033[31m{'*'*50}
An Error occured during the conversion process of {filepath} to <dest>.
[{E.__class__.__name__} at char: {self.ident_char_tag}] ->
Tag: [{self.current_tag}]
Content: |{self.current_content}|
{'*'*50}\033[0m
"""[1:-1])
    def __main_parser(self):
        # Definiere Header
        result = finditer(HEADER, self.data)
        result = [x.span() for x in result]
        for i in range(len(result)):
            header, content = result[i: i+2] if len(result[i: i+2]) == 2 else ((result[i]), (END, END))
            print(header, content)
            self.headers.append((header[0], header[1]))
            self.contents.append((header[1], content[0]))
        for h, c in zip(self.headers, self.contents):
            
            tag = self.data[h[0]:h[1]]
            content = self.data[c[0]:c[1]]
            
            self.current_tag = tag
            self.current_content = content
            self.ident_char_tag = h[0]
            self.ident_char_content = c[0]
            
            self.__parse_single(tag, content)
            
        # for c in self.contents:
            # print(self.data[c[0]:c[1]])
    
    def __add_ctx(self, text: str):
        self.ctx += text + '\n'
    
    def __parse_single(self, header: str, content: str):
        
        t= search(HEADER, header)
        groups = t.groups()
        _, tag, at, identifier, arguments = groups
        identifier = identifier[1:-1]
        arguments = arguments.split(' ')[1:]
        print(t.groups(),'\n')
        match tag:
            case 'Enable':
                if not is_empty(content):
                    raise SyntaxError
                if hasattr(self, 'SETTING_' + identifier):
                    setattr(self, 'SETTING_' + identifier, True)
                else:
                    raise SettingDoesNotExist
            case 'Use':
                if not is_empty(content):
                    raise SyntaxError
                if not self.SETTING_USAGE_ALLOWED:
                    raise UsageIsNotAllowed
                
            case 'Database':
                if not is_empty(content):
                    raise SyntaxError
                if not identifier:
                    raise IndentifierDoesNotExist
                
                name, path = identifier.split(':')
                
                if not at:
                    raise SyntaxError

                for arg in arguments:
                    if arg not in ['Backup', 'Destroy']:
                        raise ArgumentNotAllowed
                
            case 'Table':
                ctx = TableBuilder(content, identifier).ctx
                self.__add_ctx(ctx)
            case 'Build':
                if not is_empty(content):
                    raise SyntaxError
            case 'Fill':
                if not is_empty(content):
                    raise SyntaxError
            case 'Output':
                if not is_empty(content):
                    raise SyntaxError
            case 'Script':
                if not self.SETTING_SCRIPT_INJECTION_ALLOWED:
                    raise ScriptInjectionIsNotAllowed
                
                if is_empty(content):
                    raise SyntaxError
            case _:
                raise TagError
        
        
    def __parse_options(self):
        ...
            
        
Converter('base.sq')