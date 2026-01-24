import re
class PTRN:
    HEADER = "\\<Table@\'\\w+\'\\>"
    TABLE_NAME = "'[^']*'"
    DEFAULT = "(->)\\s*(?:(\"[^\"]*\")|('[^']*')|(\\d+)|(True|False|None))"
    TYPE = "(:|,)\\s*(Integer|Text|Boolean)|(Numeric|Float|DateTime)"
    AUTO = "(Primary|Nullable)"
    NAME = "[a-zA-Z_][a-zA-Z0-9_]*(?=:)"

PATH: str = './module/'

r = re.search(PTRN.AUTO, "id: Integer, Primary")

search = re.search
print(r)
class QuickSQL:
    def __init__(self, text: str):
        self.text = text
        self.ctx = ''
        self.__parse()
    def __add_ctx(self, ctx: str):
        self.ctx += ctx + '\n'
    
    def __create_column(self, line: str):
        name = search(PTRN.NAME, line)
        auto = re.findall(PTRN.AUTO, line)
        type = search(PTRN.TYPE, line)
        default = search(PTRN.DEFAULT, line)
        
        primary = False
        nullable = False
        
        if 'Nullable' in auto:
            nullable = True
        if 'Primary' in auto:
            primary = True
        
        print(name, auto, default)
        name = name.group() if name is not None else None
        type = type.group() if type is not None else None
        default = default.group() if default is not None else None
        
        
        if type.startswith(':'):
            type = type[1:].strip()
        type = type.strip()
        
        if default and default.startswith('->'):
            default = default[2:]
        
        if name is None:
            raise SyntaxError('A Name must be specified!')
        if type is None:
            raise SyntaxError('A type must be specified!')
        
        
        self.__add_ctx(f"    {name} = Column({type}{', primary_key=True' if primary else ''}{', nullable=True' if nullable else ''}{f', default={default}' if default is not None else ''})")
    
    def __parse(self):
        self.__add_ctx('from sqlalchemy import Column, Integer, String, Numeric, Boolean')
        self.__add_ctx('from src.api.sql_access import SQLA')
        lines = self.text.splitlines()
        for idx, line in enumerate(lines):
            tablename = re.search(PTRN.TABLE_NAME, line)
            if tablename:
                tablename = tablename.group()[1:-1]
                self.__add_ctx(f'class {tablename}(SQLA.base):')
                self.__add_ctx(f'    __tablename__ = \'{tablename}\'')
            else:
                self.__create_column(line)
                
with open(f'base.sq') as file:
    template = file.read()
sql = QuickSQL(template)

with open(f'db.py', 'w') as file:
    file.write(sql.ctx)