import { useState } from "react";
import "./FormContainer.css";

export function FormContainer({user,setUser,pass,setPass,onAuth }) {
  return (
    <div className="form_container">
      <div className="welcome_message">Welcome</div>
      <input 
        className="auth_input" 
        placeholder="Username" 
        value={user}
        onChange={(e)=>setUser(e.target.value)}
      />
      <input 
        className="auth_input" 
        type="password" 
        placeholder="Password" 
        value={pass}
        onChange={(e)=>setPass(e.target.value)}
      />
      <div className="button_row">
        <button
          className="signup_button"
          onClick={() => onAuth("signup")}
        >
          Sign Up
        </button>

        <button
          className="login_button"
          onClick={() => onAuth("login")}
        >
          Login
        </button>
      </div>
    </div>
  );
}
