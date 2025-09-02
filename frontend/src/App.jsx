import React, { useState } from "react";
import { login, register, logout, auth } from "./firebase";

function App() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleRegister = async () => {
    await register(email, password);
    alert("User registered!");
  };

  const handleLogin = async () => {
    await login(email, password);
    const token = await auth.currentUser.getIdToken();
    console.log("Firebase Token:", token);

    // Call Python backend
    const res = await fetch("http://127.0.0.1:8000/protected", {
      headers: { Authorization: `Bearer ${token}` }
    });
    const data = await res.json();
    console.log(data);
    alert(JSON.stringify(data));
  };

  return (
    <div>
      <h2>Next-Step Auth Test</h2>
      <input placeholder="Email" onChange={(e) => setEmail(e.target.value)} />
      <input
        type="password"
        placeholder="Password"
        onChange={(e) => setPassword(e.target.value)}
      />
      <button onClick={handleRegister}>Register</button>
      <button onClick={handleLogin}>Login</button>
      <button onClick={logout}>Logout</button>
    </div>
  );
}

export default App;
