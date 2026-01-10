from pydantic import BaseModel,Field,validator,ConfigDict
from enum import Enum
from typing import List

class User(BaseModel):
    user_id:str=Field(...,min_length=4,max_length=28)
    hashed_password:str

class UserLoginSignUp(BaseModel):
    user_id:str=Field(...,min_length=4,max_length=28)
    password:str=Field(...,min_length=6,max_length=28)

    @validator('password')
    def validate_pass_length(cls,v):
        if ((len(v.encode('utf-8')))>72):
            raise ValueError("password must be less than 72 bytes after encoding")
        return v


class MessageTypes(str,Enum):
    dm="dm"
    broadcast="broadcast"
    user_list="user_list"
    client_id="client_id"
    history="history"

class Message(BaseModel):
    message_type:MessageTypes
    sender_id:str
    reciever_id:str|None=None
    message:str

class Message_withID(Message):
    id:int
    model_config = ConfigDict(from_attributes=True)

class ChatHistory(BaseModel):
    past_history:List[Message_withID]