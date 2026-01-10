from sqlalchemy import Column,String,Integer,Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from .models import MessageTypes


Base=declarative_base()

class Users(Base):
    __tablename__="users"
    
    user_id=Column(String,primary_key=True)
    hashed_password=Column(String)

class Messages(Base):
    __tablename__="messages"
    id=Column(Integer,primary_key=True)
    message_type=Column(
        SQLEnum(MessageTypes,name="message_types"),
        nullable=False
    )
    sender_id=Column(String,nullable=False)
    reciever_id=Column(String)
    message=Column(String,nullable=False)