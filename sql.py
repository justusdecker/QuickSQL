def backup_and_remove(): ...

from sqlalchemy import create_engine, Column, Integer, String, Numeric, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



class SQLAccess:
    def __init__(self, url: str = 'sqlite:///default.db'):
        self.url = url
        self.base = declarative_base()
        self.connect()  
    
    def connect(self):
        self.engine = create_engine(self.url)
        self.base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()
    
    def close(self): # TODO: Add close
        ...
            
SQLA = SQLAccess()