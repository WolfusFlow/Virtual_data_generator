import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

hostname          = os.environ['POSTGRESQL']
database          = os.environ['DATABASE']
database_port     = os.environ['DATABASE_PORT']
database_user     = os.environ['DB_USER']
database_password = os.environ['DB_PASSWORD']
table_name        = os.environ['TABLE_NAME']

db_string = f'postgresql://{database_user}:{database_password}\
            @{hostname}:{database_port}/{database}'

engine = create_engine(db_string)
Session = sessionmaker(bind=engine)

Base = declarative_base()