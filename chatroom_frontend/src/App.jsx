import { useState,useEffect } from 'react'
import './App.css'
import { AuthPage } from './pages/AuthPage';
import { ChatroomPage } from './pages/ChatroomPage';

function App() {
  const [root_url_http,setUrlHttp]=useState("");
  const [root_url_websocket,setUrlWebsocket]=useState("");

  useEffect(() => {
    if (import.meta.env.MODE === "development") {
      setUrlWebsocket("ws://127.0.0.1:8000/ws");
      setUrlHttp("http://127.0.0.1:8000/");
    } else {
      setUrlWebsocket("wss://chatroom-as5j.onrender.com/ws");
      setUrlHttp("https://chatroom-as5j.onrender.com/");
    }
  }, []);
  const [token,setToken]=useState(localStorage.getItem("chat_token"));
  const [user,setUser]=useState(localStorage.getItem("chat_user"));

  const handleLogin=(newToken,newUser)=>{
    setToken(newToken);
    setUser(newUser);
    localStorage.setItem("chat_token",newToken);
    localStorage.setItem("chat_user",newUser);
  }
  const handleLogout=()=>{
    setToken(null);
    setUser(null);
  }

  return (
    <div className='App'>
      {token ? (
        <ChatroomPage token={token} currentUser={user} root_url_ws={root_url_websocket} onLogout={handleLogout} />
      ) : (
        <AuthPage onLoginSuccess={handleLogin} root_url_http={root_url_http} />
      )}
    </div>
  )
}

export default App
