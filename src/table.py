from re import finditer
from src.utils import Context, none_to_str, is_empty
from src.constants import TABLE

class TableBuilder(Context):
    def __init__(self, content: str, identifier: str):
        super().__init__()
        self.content = content
        self.identifier = identifier
        
    def __parse(self):
        if is_empty(self.content):
            raise SyntaxError
        t = finditer(TABLE, self.content)
        new_ctx = TableBuilder.build_header(self.identifier)
        self.add_ctx(new_ctx)
        for x in t:
            name, _, applier, type, sep1, constraint1, sep2, constraint2, default_str1, default_str2, default_int, default_bool = x.groups()
            
            #! TODO: '' defaults are not taken into account
            if constraint1 is None: constraint1 = ''
            if constraint2 is None: constraint2 = ''
            default = none_to_str(*[default_bool, default_int, default_str1, default_str2])
            nullable = 'Nullable' in constraint1 or 'Nullable' in constraint2
            primary = 'Primary' in constraint1 or 'Primary' in constraint2
            new_ctx = TableBuilder.build_column(name, type, primary, nullable, default)
            self.add_ctx(new_ctx)
        print(self.ctx)

    @staticmethod
    def build_column(name, type, primary, nullable, default):
        build = (" " * 4) + f'{name} = '
        build += f"Column({type}{', primary_key = True' if primary else ''}{', nullable = True' if nullable else ''}{f', default = {default}' if default else ''})"   
        return build
    
    @staticmethod
    def build_header(tablename: str):
        return f'class {tablename}(Base):\n{" "*4}__tablename__ = {tablename}'