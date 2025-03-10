import { useState, useEffect } from "react";
import { useDrag, useDrop } from "react-dnd";
import { getSquad, updateStartingXI, generateStartingXIGraphic } from "../services/club";
import { getToken } from "../services/auth";
import { useNavigate } from "react-router-dom";

// ✅ Function to trigger image download
const downloadImage = async (url, filename) => {
  try {
    const response = await fetch(url);
    const blob = await response.blob();
    const link = document.createElement("a");

    link.href = URL.createObjectURL(blob);
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    // Clean up object URL
    URL.revokeObjectURL(link.href);
  } catch (error) {
    console.error("❌ Error downloading image:", error);
    alert("Failed to download image.");
  }
};

// ✅ PlayerItem Component (Drag & Drop)
const PlayerItem = ({ player }) => {
  const [{ isDragging }, drag] = useDrag(() => ({
    type: "PLAYER",
    item: { id: player.id, name: player.name, position: player.position },
    collect: (monitor) => ({
      isDragging: !!monitor.isDragging(),
    }),
  }));

  return (
    <div ref={drag} className={`p-2 border rounded cursor-pointer ${isDragging ? "opacity-50" : "bg-gray-100"}`}>
      {player.name} - {player.position}
    </div>
  );
};

// ✅ StartingXI Component (Drop Area)
const StartingXI = ({ players, moveToSquad }) => {
  const [{ isOver }, drop] = useDrop(() => ({
    accept: "PLAYER",
    drop: (item) => moveToSquad(item.id),
    collect: (monitor) => ({
      isOver: !!monitor.isOver(),
    }),
  }));

  return (
    <div ref={drop} className={`p-4 border-2 ${isOver ? "border-blue-400" : "border-gray-300"} rounded min-h-[200px]`}>
      <h2 className="text-xl font-bold">Starting XI</h2>
      {players.length === 0 ? (
        <p className="text-gray-500">Drag players here</p>
      ) : (
        players.map((player) => (
          <div key={player.id} className="p-2 bg-green-200 rounded mb-2">
            {player.name} - {player.position}
            <button className="ml-2 btn btn-sm btn-error" onClick={() => moveToSquad(player.id)}>
              Remove
            </button>
          </div>
        ))
      )}
    </div>
  );
};

// ✅ Main Page Component
export default function StartingXIPage() {
  const [squad, setSquad] = useState([]);
  const [startingXI, setStartingXI] = useState([]);
  const [imageUrl, setImageUrl] = useState(""); // Store the generated graphic URL
  const token = getToken();
  const navigate = useNavigate();

  useEffect(() => {
    getSquad(token).then((response) => {
      if (response.data) {
        setSquad(response.data);
        setStartingXI(response.data.filter((player) => player.is_starting_xi));
      }
    });
  }, [token]);

  // ✅ Move player to Starting XI
  const moveToXI = (playerId) => {
    if (startingXI.length >= 11) return alert("You can only select 11 players!");
    const player = squad.find((p) => p.id === playerId);
    if (player) {
      setStartingXI([...startingXI, player]);
      setSquad(squad.filter((p) => p.id !== playerId));
    }
  };

  // ✅ Remove player from Starting XI back to squad
  const moveToSquad = (playerId) => {
    const player = startingXI.find((p) => p.id === playerId);
    if (player) {
      setSquad([...squad, player]);
      setStartingXI(startingXI.filter((p) => p.id !== playerId));
    }
  };

  // ✅ Generate Graphic from Starting XI
  const generateGraphic = async () => {
    try {
      const response = await generateStartingXIGraphic(token, startingXI.map((p) => p.name));
      setImageUrl(response.data.image_url);
    } catch (error) {
      console.error("❌ Error generating graphic:", error);
      alert("Failed to generate graphic.");
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100">
      <h1 className="text-3xl font-bold">Starting XI Selection</h1>

      {/* Squad List */}
      <div className="flex gap-4 mt-4">
        <div className="p-4 border rounded w-1/3">
          <h2 className="text-xl font-bold">Squad</h2>
          {squad.length > 0 ? (
            squad.map((player) => (
              <div key={player.id} onClick={() => moveToXI(player.id)}>
                <PlayerItem player={player} />
              </div>
            ))
          ) : (
            <p className="text-gray-500">No players available</p>
          )}
        </div>

        {/* Drag & Drop Starting XI */}
        <StartingXI players={startingXI} moveToSquad={moveToSquad} />
      </div>

      {/* Generate Graphic Button */}
      <button className="btn btn-primary mt-4" onClick={generateGraphic}>
        Generate Graphic
      </button>
          {/* ✅ Download Button */}
          <button className="btn btn-success mt-4" onClick={() => downloadImage(imageUrl, "Starting_XI.png")}>
            Download Image
          </button>
      {/* Display Generated Graphic */}
      {imageUrl && (
        <div className="mt-4">
          <h2 className="text-xl font-bold">Generated Graphic:</h2>
          <img src={imageUrl} alt="Starting XI Graphic" className="mt-2 border-2 border-gray-300 rounded" />
        </div>
      )}
    </div>
  );
}
