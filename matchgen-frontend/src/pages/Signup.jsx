import { useState } from "react";
import { register } from "../services/auth";
import { useNavigate } from "react-router-dom";

export default function Signup() {
  const [signupData, setSignupData] = useState({ username: "", email: "", password: "" });
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  const handleSignup = async () => {
    const response = await register(signupData.username, signupData.email, signupData.password);
    if (response.success) {
      setMessage("✅ Registration successful! Redirecting to login...");
      setTimeout(() => navigate("/login"), 2000); // Redirect to login page after signup
    } else {
      setMessage("❌ " + response.error);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100">
      <h1 className="text-4xl font-bold text-blue-600">🚀 Signup</h1>
      <div className="mt-6 flex flex-col gap-2">
        <input
          type="text"
          placeholder="Username"
          className="input input-bordered"
          value={signupData.username}
          onChange={(e) => setSignupData({ ...signupData, username: e.target.value })}
        />
        <input
          type="email"
          placeholder="Email"
          className="input input-bordered"
          value={signupData.email}
          onChange={(e) => setSignupData({ ...signupData, email: e.target.value })}
        />
        <input
          type="password"
          placeholder="Password"
          className="input input-bordered"
          value={signupData.password}
          onChange={(e) => setSignupData({ ...signupData, password: e.target.value })}
        />
        <button className="btn btn-primary" onClick={handleSignup}>Sign Up</button>
      </div>
      <p className="mt-4 text-lg bg-white p-4 rounded shadow">{message}</p>
    </div>
  );
}
