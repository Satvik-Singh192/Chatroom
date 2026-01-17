import { useEffect, useState,useRef } from "react";
import { ActiveUserContainer } from "../components/chatroom/ActiveUserContainer";
import { ChatContainer } from "../components/chatroom/ChatContainer";
import "./ChatroomPage.css";



export function ChatroomPage({ token, currentUser, root_url_ws, onLogout }) {
    const [onlineUsers,setOnlineUsers]=useState([]);
    const [messages,setMessages]=useState([]);
    const wsRef=useRef(null);
    const historyLoadedRef=useRef(false);

    const handleLogout = () => {
        if(wsRef.current) {
            wsRef.current.close();
        }
        localStorage.removeItem("chat_token");
        localStorage.removeItem("chat_user");
        onLogout();
    };


    useEffect(()=>{
        if(!token)return;
        const websocket_url=`${root_url_ws}?token=${token}`;
        const ws=new WebSocket(websocket_url);
        wsRef.current=ws;

        ws.onopen=()=>{
            console.log("websocket connected");
        };
        ws.onmessage=(event)=>{
            const data=JSON.parse(event.data);
            switch(data.message_type){
                case "user_list":{
                    const userArray=JSON.parse(data.message);
                    setOnlineUsers(userArray);
                    break;
                }
                case "history":{
                    if(!historyLoadedRef.current) {
                        const history=JSON.parse(data.message);
                        setMessages(Array.isArray(history) ? history : []);
                        historyLoadedRef.current = true;
                    }
                    break;
                }
                case "broadcast":
                case "dm":{
                    setMessages(prev=>[...prev,data]);
                    break;
                }
                default:{
                    console.warn("unknow message type recieved: ",data.message_type," ",data.message);
                }
            }
        }
        ws.onerror=(error)=>{
            console.error("Websoclet error in ChatroomPage.jsx: ",error );
        }
        ws.onclose=()=>{
            console.log("logged out successfully");
        }

        return ()=>{
            ws.close();
            wsRef.current=null;
        }
        
    },[token,root_url_ws]);
    

    const sendMessage=(text,reciever)=>{
        if(!wsRef.current||wsRef.current.readyState!==WebSocket.OPEN){
            console.log("send message function return ");
            return;
        }
        let payload;

        if(reciever==="all"){
            payload={
                    message_type:"broadcast",
                    sender_id:currentUser,
                    reciever_id:null,
                    message:text
                };
        }
        else{
                payload = {
                message_type: "dm",
                sender_id: currentUser,
                reciever_id: reciever,
                message: text
            };
        }
        wsRef.current.send(JSON.stringify(payload));
        setMessages(prev=>[...prev,payload]);
    };
    
    return(
        <div className="ChatroomPage">
            <div className="ActiveUserContainer">
                <ActiveUserContainer
                    users={onlineUsers}
                    currentUser={currentUser}
                />
            </div>
            <div className="ChatContainerWrapper">
                <div className="ChatHeader">
                    <span className="ConnectionStatus">Connected as {currentUser}</span>
                    <button className="LogoutButton" onClick={handleLogout}>Logout</button>
                </div>
                <ChatContainer
                    messages={messages}
                    onlineUsers={onlineUsers}
                    currentUser={currentUser}
                    onSend={sendMessage}
                />
            </div>
        </div>
    );
}