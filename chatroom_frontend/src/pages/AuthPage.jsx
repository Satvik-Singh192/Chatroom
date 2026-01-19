import { useState } from "react";
import { FormContainer } from "../components/auth/FormContainer";
import "./AuthPage.css";

export function AuthPage({root_url_http,onLoginSuccess}){
    const [user,setUser]=useState("");
    const [pass,setPass]=useState("");
    const [error,setError]=useState("");

    const handleAuth=async (type)=>{
        let url=root_url_http+type;
        try{
            const response=await fetch(url,{
                method:'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_id: user, password: pass }),
                credentials:"include"
            });
            const data=await response.json();
            if(type=="signup"){
                throw new Error(data.status||data.detail);
            }
            if(!response.ok)throw new Error(data.detail||"something went wrong, index 117");
            if(type=="login"){
                onLoginSuccess();
            }
        }
        catch(err){
            setError(err.message);
        }
    }

    return(
        <div className="auth_page">
            <FormContainer
                user={user}
                setUser={setUser}
                pass={pass}
                setPass={setPass}
                onAuth={handleAuth}
            />
            {error && <p style={{ color: 'red' }}>{error}</p>}
        </div>
    )
}