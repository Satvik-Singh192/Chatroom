import { useState } from "react";
import "./ChatContainer.css";

export function ChatContainer({messages,onlineUsers,currentUser,onSend}){
    const [text,setText]=useState("");
    const [receiver,setReceiver]=useState("all");

    const handleSubmit=()=>{
        if(!text.trim())return;
        onSend(text,receiver);
        setText("");
    }

    return (
        <div className="ChatContainer">
            <ul className="ChatMessages">
                {
                    messages.map((msg,index)=>{
                        if(msg.sender_id==="server"){
                            return(
                                <li key={index} className="msg-system">
                                    [SYSTEM]: {msg.message}
                                </li>
                            );
                        }
                        if(msg.sender_id===currentUser){
                            return(
                                <li key={index} className="msg-self">
                                    {msg.message}
                                </li>
                            );
                        }
                        return(
                            <li key={index} className="msg-user">
                                User {msg.sender_id}: {msg.message}
                            </li>
                        );
                    })
                }
            </ul>
            <div className="ChatInputRow">
                <input
                 className="ChatInput"
                 placeholder="Type message"
                 value={text}
                 onChange={(e)=>setText(e.target.value)}
                 />

                 <select
                className="ReceiverSelect"
                value={receiver}
                onChange={(e) => setReceiver(e.target.value)}
                >
                <option value="all">All</option>
                {onlineUsers
                    .filter(u => u !== currentUser)
                    .map(u => (
                    <option key={u} value={u}>
                        User {u}
                    </option>
                    ))}
                </select>
                <button className="SendButton" onClick={handleSubmit}>
                Send
                </button>

            </div>
        </div>
    )
}