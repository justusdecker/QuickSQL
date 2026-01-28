class Context:
    def __init__(self):
        self.ctx = ''
    def add_ctx(self, text: str):
        self.ctx += text + '\n'
        
def is_empty(text: str) -> bool:
    return text.isspace() or not text or text == '\n'

def none_to_str(*values):
    values = [x if x is not None else '' for x in values]
    return "".join(values)