from sqlalchemy import Column,String
from sqlalchemy.ext.declarative import declarative_base


Base=declarative_base()

class Users(Base):
    __tablename__="Users"
    
    user_id=Column(String,primary_key=True)
    hashed_password=Column(String)

