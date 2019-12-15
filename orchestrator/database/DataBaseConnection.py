import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import VirtualData

class DataBaseConnection():

    def __init__(self):
        self.hostname          = os.environ['POSTGRESQL']
        self.database          = os.environ['DATABASE']
        self.database_port     = os.environ['DATABASE_PORT']
        self.database_user     = os.environ['DB_USER']
        self.database_password = os.environ['DB_PASSWORD']
        self.table_name        = os.environ['TABLE_NAME']

    
    engine  = None
    session = None

    
    def connect(self):
        db_string = f'postgresql://{self.database_user}:{self.database_password}\
                    @{self.hostname}:{self.database_port}/{self.database}'

        self.engine = create_engine(db_string)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        
    def write_to_database(self, message):
        insert_message = VirtualData(message)
        self.session.add(insert_message)
        self.session.commit()

    def close(self):
        self.session.close()
