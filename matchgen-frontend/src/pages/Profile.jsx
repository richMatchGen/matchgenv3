import { useState, useEffect } from "react";
import { getProfile, updateProfile, changePassword, getToken } from "../services/auth";

export default function Profile() {
  const [profile, setProfile] = useState({ username: "", email: "" });
  const [message, setMessage] = useState("");
  const token = getToken();

  useEffect(() => {
    const fetchProfile = async () => {
      const response = await getProfile(token);
      if (response.success) {
        setProfile(response.data);
      } else {
        setMessage("❌ " + response.error);
      }
    };
    fetchProfile();
  }, []);

  const handleUpdateProfile = async () => {
    const response = await updateProfile(token, profile);
    setMessage(response.success ? "✅ Profile updated!" : "❌ " + response.error);
  };

  const handleChangePassword = async (oldPassword, newPassword) => {
    const response = await changePassword(token, oldPassword, newPassword);
    setMessage(response.success ? "✅ Password updated!" : "❌ " + response.error);
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100">
      <h1 className="text-4xl font-bold text-blue-600">👤 User Profile</h1>
      <div className="mt-6 flex flex-col gap-2">
        <input
          type="text"
          placeholder="Username"
          className="input input-bordered"
          value={profile.username}
          onChange={(e) => setProfile({ ...profile, username: e.target.value })}
        />
        <input
          type="email"
          placeholder="Email"
          className="input input-bordered"
          value={profile.email}
          onChange={(e) => setProfile({ ...profile, email: e.target.value })}
        />
        <button className="btn btn-primary" onClick={handleUpdateProfile}>Update Profile</button>
      </div>

      <h2 className="mt-6 text-2xl font-bold">Change Password</h2>
      <div className="mt-3 flex flex-col gap-2">
        <input type="password" placeholder="Old Password" id="oldPass" className="input input-bordered" />
        <input type="password" placeholder="New Password" id="newPass" className="input input-bordered" />
        <button className="btn btn-error" onClick={() => handleChangePassword(
          document.getElementById("oldPass").value,
          document.getElementById("newPass").value
        )}>Change Password</button>
      </div>

      <p className="mt-4 text-lg bg-white p-4 rounded shadow">{message}</p>
    </div>
  );
}
