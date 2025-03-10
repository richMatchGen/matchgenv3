import { useState, useEffect } from "react";
import { getSquad } from "../services/club";
import { getToken } from "../services/auth";
import { useNavigate } from "react-router-dom";
import { addPlayer } from "../services/club";  // ✅ Ensure this is correctly imported


export default function Squad() {
  const [squad, setSquad] = useState([]);
  const [error, setError] = useState("");
  const token = getToken();
  const [newPlayer, setNewPlayer] = useState({ name: "", position: "" });
  const navigate = useNavigate();

  useEffect(() => {
    if (!token) {
      setError("User not authenticated. Redirecting to login...");
      setTimeout(() => navigate("/login"), 2000);
      return;
    }

    getSquad(token)
      .then((response) => setSquad(response.data))
      .catch((err) => {
        console.error("Error fetching squad:", err);
        setError("Failed to load squad. Please log in again.");
        setTimeout(() => navigate("/login"), 2000);
      });
  }, [token, navigate]);

    const handleAddPlayer = async () => {
    await addPlayer(token, newPlayer);
    setNewPlayer({ name: "", position: "" });
  };

// //   return (
//     <div>
//       <h1>Squad Management</h1>
//       {error && <p className="text-red-500">{error}</p>}
//       <ul>
//         {squad.map((player) => (
//           <li key={player.id}>{player.name} - {player.position}</li>
//         ))}
//       </ul>
//     </div>
//   );
// // }

  return (
    <div>
<div className="p-4 border rounded w-1/3">
  <h2 className="text-xl font-bold">Squad</h2>
</div>
      <ul>
        {squad.map(player => (
          <li key={player.id}>{player.name} - {player.position}</li>
        ))}
      </ul>
      <input placeholder="Player Name" class="input input-bordered" value={newPlayer.name} onChange={e => setNewPlayer({ ...newPlayer, name: e.target.value })} />
      <input placeholder="Position" class="input input-bordered" value={newPlayer.position} onChange={e => setNewPlayer({ ...newPlayer, position: e.target.value })} />
      <button className="btn btn-primary" onClick={handleAddPlayer}>Add Player</button>
    </div>
  );
}
