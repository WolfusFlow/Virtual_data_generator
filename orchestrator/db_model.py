import os

from database import Base

from sqlalchemy import Column, String, Integer

class VirtualData(Base):
    __tablename__ = os.environ['TABLE_NAME']

    id          = Column(Integer, primary_key=True)
    uuid        = Column(String)
    server_name = Column(String)
    data_type   = Column(String)
    value       = Column(String)
    created_at  = Column(String)

    def __init__(self, uuid, server_name, data_type, value, created_at):
        self.uuid        = uuid
        self.server_name = server_name
        self.data_type   = data_type
        self.value       = value
        self.created_at  = created_at