import { useState } from "react";
import { login, getToken } from "../services/auth";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const [credentials, setCredentials] = useState({ username: "", password: "" });
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  const handleLogin = async () => {
    const response = await login(credentials.username, credentials.password);
    if (response.success) {
      setMessage("✅ Login successful!");
      navigate("/dashboard"); // Redirect to dashboard after login
    } else {
      setMessage("❌ " + response.error);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100">
      <h1 className="text-4xl font-bold text-blue-600">🚀 Login</h1>
      <div className="mt-6 flex flex-col gap-2">
        <input
          type="text"
          placeholder="Username"
          className="input input-bordered"
          value={credentials.username}
          onChange={(e) => setCredentials({ ...credentials, username: e.target.value })}
        />
        <input
          type="password"
          placeholder="Password"
          className="input input-bordered"
          value={credentials.password}
          onChange={(e) => setCredentials({ ...credentials, password: e.target.value })}
        />
        <button className="btn btn-primary" onClick={handleLogin}>Login</button>
      </div>
      <p className="mt-4 text-lg bg-white p-4 rounded shadow">{message}</p>
    </div>
  );
}
