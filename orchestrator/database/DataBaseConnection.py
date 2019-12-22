import os
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import VirtualData

logging.basicConfig(filename=__name__,
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s \n\n',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

class DataBaseConnection():

    def __init__(self, *args, **kwargs):
        try:
            self.hostname          = kwargs['POSTGRESQL']
            self.database          = kwargs['DATABASE']
            self.database_port     = kwargs['DATABASE_PORT']
            self.database_user     = kwargs['DB_USER']
            self.database_password = kwargs['DB_PASSWORD']
            self.table_name        = kwargs['TABLE_NAME']
        except KeyError as ke:
            logging.exception(f'Exception in DataBaseConnection Initialization:\n {ke}')

    engine  = None
    session = None

    
    def connect(self):
        db_string = f'postgresql://{self.database_user}:{self.database_password}\
                    @{self.hostname}:{self.database_port}/{self.database}'

        self.engine = create_engine(db_string)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        
    def write_to_database(self, message):
        insert_message = VirtualData(**message)
        self.session.add(insert_message)
        self.session.commit()

    def close(self):
        self.session.close()
