import os

from DataBaseConnection import Base

from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

class VirtualData(declarative_base):
    __tablename__ = os.environ['TABLE_NAME']

    id          = Column(Integer, primary_key=True)
    uuid        = Column(String)
    server_name = Column(String)
    data_type   = Column(String)
    value       = Column(String)
    created_at  = Column(String)

    def __init__(self, *args, **kwargs):
        self.uuid        = kwargs['uuid']
        self.server_name = kwargs['server_name']
        self.data_type   = kwargs['data_type']
        self.value       = kwargs['value']
        self.created_at  = kwargs['created_at']