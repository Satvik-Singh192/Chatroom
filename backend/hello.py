from fastapi import FastAPI,WebSocket,WebSocketDisconnect,HTTPException,Query,Depends
from fastapi.middleware.cors import CORSMiddleware
import json
from .models import Message,MessageTypes,UserLoginSignUp
from .jwt import hash_password,verify_password,create_jwt_token,decode_jwt
from .database import engine,get_db
from backend import database_models
from sqlalchemy.orm import Session 

database_models.Base.metadata.create_all(bind=engine)

app=FastAPI()
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "*", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ConnectionManager:
    def __init__(self):
        self.active_connections:dict[str,WebSocket]={}
    
    async def connect(self,user_id,websocket:WebSocket)->str:
        await websocket.accept()
        self.active_connections[user_id]=websocket
        await self.send_user_list();
        await self.broadcast(Message(message_type=MessageTypes.broadcast,sender_id="server",reciever_id=None,message=f"user {user_id} has joined the chat"))
    
    def get_websocket(self,client_id:str):
        if client_id not in self.active_connections:
            raise ValueError(f"client with id {client_id} does not exist")
        return self.active_connections[client_id]

    async def disconnect(self,client_id:str):
        if client_id not in self.active_connections:
            raise ValueError(f"client with {client_id} already does not exist")
        del self.active_connections[client_id]
        await self.send_user_list();
        await manager.broadcast(Message(message_type="broadcast",sender_id="server",reciever_id=None,message=f"user #{client_id} has left the chat"))
    
    async def send_personal_message(self, msg: Message):
        receiver_ws = self.active_connections.get(msg.reciever_id)
        if receiver_ws:
            await receiver_ws.send_json(msg.model_dump())

    async def broadcast(self,message:Message):
        for client in self.active_connections.keys():
            if client==message.sender_id:
                continue
            connection=self.active_connections[client]
            await connection.send_json(message.model_dump())
    
    async def send_user_list(self):
        msg = Message(
            message_type=MessageTypes.user_list,
            sender_id="server",
            reciever_id=None,
            message=json.dumps(list(self.active_connections.keys()))
        )
        await self.broadcast(msg)

manager=ConnectionManager()

@app.post("/signup")
def signup(user_data:UserLoginSignUp,db:Session=Depends(get_db)):
    user=db.query(database_models.Users).filter(database_models.Users.user_id==user_data.user_id).first()
    if user!=None:
        raise HTTPException(status_code=409,detail="User already exists")
    hashed_pwd=hash_password(user_data.password)
    user_insert=database_models.Users(user_id=user_data.user_id,hashed_password=hashed_pwd)
    db.add(user_insert)
    db.commit()
    return {"status":"success"}


@app.post("/login")
def login(user_data:UserLoginSignUp,db:Session=Depends(get_db)):
    user=db.query(database_models.Users).filter(database_models.Users.user_id==user_data.user_id).first()
    if not user:
        raise HTTPException(status_code=404,detail="user not found")
    if verify_password(pass_to_check=user_data.password,hashed_password=user.hashed_password)==False:
        raise HTTPException(status_code=404,detail="invalid credentials")
    token=create_jwt_token(user_data)
    return {"access_token":token}

@app.websocket("/ws")
async def websocket_endpoint(websocket:WebSocket,token:str=Query(None)):
    #await websocket.accept()
    if token is None:
        await websocket.close(code=1008)
        return
    user_id_frmjwt=decode_jwt(token)
    if user_id_frmjwt is None:
        await websocket.close(code=1008,reason="TOKEN EXPIRED")
        return
    
    await manager.connect(user_id_frmjwt,websocket)
    try:
        while True:
            data=await websocket.receive_json()
            msg=Message(**data)
            msg.sender_id = user_id_frmjwt

            if msg.message_type==MessageTypes.dm:
                await manager.send_personal_message(msg)
            elif msg.message_type==MessageTypes.broadcast:
                await manager.broadcast(msg)
    except WebSocketDisconnect:
            await manager.disconnect(user_id_frmjwt)


