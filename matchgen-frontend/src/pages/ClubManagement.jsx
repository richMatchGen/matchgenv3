import { useState, useEffect } from "react";
import { getClub } from "../services/club";
import { getToken } from "../services/auth";
import { useNavigate } from "react-router-dom";

export default function ClubManagement() {
  const [club, setClub] = useState(null);
  const [error, setError] = useState("");
  const token = getToken();
  const navigate = useNavigate();

  useEffect(() => {
    if (!token) {
      console.log("❌ No token found, redirecting to login...");
      setError("User not authenticated. Redirecting to login...");
      setTimeout(() => navigate("/login"), 2000);
      return;
    }

    getClub(token)
      .then((response) => {
        console.log("✅ Club Data Fetched:", response.data);
        setClub(response.data);
      })
      .catch((err) => {
        console.error("❌ Error fetching club:", err);
        if (err.response?.status === 401) {
          setError("Session expired. Redirecting to login...");
          setTimeout(() => navigate("/login"), 2000);
        } else if (err.response?.status === 404) {
          setError("No club found. Create a club first.");
        } else {
          setError("Failed to load club data.");
        }
      });
  }, [token, navigate]);

  return (
    <div>
      <h1>Club Management</h1>
      {error && <p className="text-red-500">{error}</p>}
      {club ? (
        <div>
          <h2>{club.name}</h2>
          <img src={club.logo} alt="Club Logo" className="mt-4 h-24 w-24 rounded-full" />
        </div>
      ) : (
        <p>Loading club details...</p>
      )}
    </div>
  );
}
