import { useState,useEffect } from 'react'
import './App.css'
import { AuthPage } from './pages/AuthPage';
import { ChatroomPage } from './pages/ChatroomPage';

function App() {
  const [root_url_http,setUrlHttp]=useState("");
  const [root_url_websocket,setUrlWebsocket]=useState("");
  const [currentUser,setCurrentUser]=useState("guest");
  const [isAuthenticated,setIsAuthenticated]=useState(false);
  const [isCheckingAuth,setIsCheckingAuth]=useState(true);

  useEffect(() => {
    if (import.meta.env.MODE === "development") {
      setUrlWebsocket("ws://127.0.0.1:8000/ws");
      setUrlHttp("http://127.0.0.1:8000/");
    } else {
      setUrlWebsocket("wss://chatroom-as5j.onrender.com/ws");
      setUrlHttp("https://chatroom-as5j.onrender.com/");
    }
  }, []);
  useEffect(() => {
    const checkAuth = async () => {
      try {
        const response = await fetch(`${root_url_http}verify`, {
          method: 'GET',
          credentials: 'include'
        });
        if (response.ok) {
          setIsAuthenticated(true);
        } else {
          setIsAuthenticated(false);
        }
      } catch (error) {
        console.log("Auth check failed:",error);
        setIsAuthenticated(false);
      } finally {
        setIsCheckingAuth(false);
      }
    };
    if (root_url_http) {
      checkAuth();
    }
  }, [root_url_http]);
  const handleLogin=()=>{
    setIsAuthenticated(true);
  };
  const handleLogout=async ()=>{
    await fetch(`${root_url_http}logout`,{
      method:"POST",
      credentials:"include"
  });
  setIsAuthenticated(false);
  setCurrentUser("");
  }

  return (
    <div className='App'>
      {isCheckingAuth ? (
        <div>Loading...</div>
      ) : isAuthenticated ? (
        <ChatroomPage root_url_ws={root_url_websocket} onLogout={handleLogout} currentUser={currentUser} setCurrentUser={setCurrentUser}/>
      ) : (
        <AuthPage onLoginSuccess={handleLogin} root_url_http={root_url_http} />
      )}
    </div>
  )
}

export default App
