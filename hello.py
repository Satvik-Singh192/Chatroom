from fastapi import FastAPI,WebSocket,WebSocketDisconnect
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from enum import Enum
import json

class MessageTypes(str,Enum):
    self_message="self_message"
    dm="dm"
    broadcast="broadcast"
    user_list="user_list"

class Message(BaseModel):
    message_type:MessageTypes
    sender_id:int
    reciever_id:int|None=None
    message:str

app=FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections:dict[int,WebSocket]={}
    
    async def connect(self,websocket:WebSocket,client_id:int):
        await websocket.accept()
        self.active_connections[client_id]=websocket
        await self.send_user_list();
    
    def get_websocket(self,client_id:int):
        if client_id not in self.active_connections:
            raise ValueError(f"client with id {client_id} does not exist")
        return self.active_connections[client_id]

    async def disconnect(self,client_id:int):
        if client_id not in self.active_connections:
            raise ValueError(f"client with {client_id} already does not exist")
        del self.active_connections[client_id]
        await self.send_user_list();
    
    async def send_personal_message(self, msg: Message):
        receiver_ws = self.active_connections.get(msg.reciever_id)
        if receiver_ws:
            await receiver_ws.send_json(msg.model_dump())

    async def broadcast(self,message:Message):
        for client in self.active_connections.keys():
            connection=self.active_connections[client]
            await connection.send_json(message.model_dump())
    
    async def send_user_list(self):
        msg = Message(
            message_type=MessageTypes.user_list,
            sender_id=0,
            reciever_id=None,
            message=json.dumps(list(self.active_connections.keys()))
        )
        await self.broadcast(msg)

manager=ConnectionManager()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket:WebSocket,client_id:int):
    await manager.connect(websocket,client_id)
    try:
        while True:
            data=await websocket.receive_json()
            msg=Message(**data)
            msg.sender_id=client_id

            if msg.message_type==MessageTypes.dm:
                await manager.send_personal_message(msg)
            elif msg.message_type==MessageTypes.broadcast:
                await manager.broadcast(msg)
    except WebSocketDisconnect:
            await manager.disconnect(client_id)
            await manager.broadcast(Message(message_type="broadcast",sender_id=client_id,reciever_id=None,message=f"user #{client_id} has left the chat"))


