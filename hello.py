from fastapi import FastAPI,WebSocket,WebSocketDisconnect
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from enum import Enum
import json
import string
import secrets


class MessageTypes(str,Enum):
    dm="dm"
    broadcast="broadcast"
    user_list="user_list"
    client_id="client_id"

class Message(BaseModel):
    message_type:MessageTypes
    sender_id:str
    reciever_id:str|None=None
    message:str

def randstr(length=8):
    alphabet=string.ascii_lowercase+string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


app=FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections:dict[str,WebSocket]={}
    
    async def connect(self,websocket:WebSocket)->str:
        await websocket.accept()
        client_id:str=randstr();
        self.active_connections[client_id]=websocket
        client_id_mssg=Message(message_type=MessageTypes.client_id,sender_id="server",reciever_id=client_id,message=f"{client_id}")
        await self.send_personal_message(client_id_mssg)
        await self.send_user_list();
        await self.broadcast(Message(message_type=MessageTypes.broadcast,sender_id="server",reciever_id=None,message=f"user {client_id} has joined the chat"))
        return client_id
    
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

@app.websocket("/ws")
async def websocket_endpoint(websocket:WebSocket):
    client_id=await manager.connect(websocket)
    try:
        while True:
            data=await websocket.receive_json()
            msg=Message(**data)
            msg.sender_id = client_id

            if msg.message_type==MessageTypes.dm:
                await manager.send_personal_message(msg)
            elif msg.message_type==MessageTypes.broadcast:
                await manager.broadcast(msg)
    except WebSocketDisconnect:
            await manager.disconnect(client_id)


