from sqlalchemy import Column,String,Integer,Date
from login.create_db_login import BaseLogin


class Login(BaseLogin):
    __tablename__ = 'userData'
    id = Column(Integer,primary_key=True, index=True)
    date = Column(Date,index=True)
    username = Column(String(20),nullable=False)
    password = Column(String(20), nullable=False)
