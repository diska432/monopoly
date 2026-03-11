import React, { useMemo, useState } from "react";
import { RoomInfo } from "../types/game";

interface JoinLobbyScreenProps {
  rooms: RoomInfo[];
  onJoin: (room: RoomInfo, password?: string) => void;
  onRefresh: () => void;
  onBack: () => void;
  error: string;
  joining: boolean;
}

const JoinLobbyScreen: React.FC<JoinLobbyScreenProps> = ({
  rooms,
  onJoin,
  onRefresh,
  onBack,
  error,
  joining,
}) => {
  const [tab, setTab] = useState<"public" | "private">("public");
  const [search, setSearch] = useState("");
  const [selectedPrivateRoomId, setSelectedPrivateRoomId] = useState<string | null>(null);
  const [password, setPassword] = useState("");

  const filteredRooms = useMemo(() => {
    const lowered = search.trim().toLowerCase();
    return rooms.filter((room) => {
      if (room.visibility !== tab) return false;
      if (!lowered) return true;
      return (
        room.name.toLowerCase().includes(lowered) ||
        room.host_name.toLowerCase().includes(lowered)
      );
    });
  }, [rooms, search, tab]);

  return (
    <div className="join-lobby-screen">
      <button className="go-back" onClick={onBack}>[ Go Back ]</button>

      <div className="join-lobby-screen__panel">
        <div className="join-lobby-screen__header">
          <div className="join-lobby-screen__tabs">
            <button
              className={`join-lobby-screen__tab ${tab === "public" ? "active" : ""}`}
              onClick={() => setTab("public")}
            >
              Public Rooms
            </button>
            <button
              className={`join-lobby-screen__tab ${tab === "private" ? "active" : ""}`}
              onClick={() => setTab("private")}
            >
              Private Rooms
            </button>
          </div>
          <div className="join-lobby-screen__search">
            <span className="join-lobby-screen__search-icon">&#x1F50D;</span>
            <input
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="SEARCH..."
            />
          </div>
        </div>

        <div className="join-lobby-screen__table-header">
          <span className="join-lobby-screen__col-name">Lobby Name</span>
          <span className="join-lobby-screen__col-max">Max</span>
          <span className="join-lobby-screen__col">Casino</span>
          <span className="join-lobby-screen__col">Mode</span>
          <span className="join-lobby-screen__col">Timer</span>
          <span className="join-lobby-screen__col">Action</span>
        </div>

        <div className="join-lobby-screen__table-body">
          {filteredRooms.length === 0 ? (
            <div className="join-lobby-screen__empty">
              <p>No rooms found yet.</p>
              <p>Try refreshing or switching tabs.</p>
            </div>
          ) : (
            filteredRooms.map((room) => {
              const isSelectedPrivate = selectedPrivateRoomId === room.id;
              return (
                <div key={room.id} className="join-lobby-screen__room-row">
                  <span className="join-lobby-screen__col-name join-lobby-screen__room-name">
                    {room.name}
                  </span>
                  <span className="join-lobby-screen__col-max">{room.player_count} / {room.max_players}</span>
                  <span className="join-lobby-screen__col">{room.casino ? "ON" : "OFF"}</span>
                  <span className="join-lobby-screen__col">{room.teams ? "TEAMS" : "1V1"}</span>
                  <span className="join-lobby-screen__col">{room.timer ? "ON" : "OFF"}</span>
                  <span className="join-lobby-screen__col join-lobby-screen__room-action">
                    {room.visibility === "public" ? (
                      <button
                        className="btn-secondary join-lobby-screen__inline-join"
                        onClick={() => onJoin(room)}
                        disabled={joining}
                      >
                        Join
                      </button>
                    ) : (
                      <button
                        className="btn-secondary join-lobby-screen__inline-join"
                        onClick={() => {
                          setSelectedPrivateRoomId(room.id);
                          setPassword("");
                        }}
                        disabled={joining}
                      >
                        Enter
                      </button>
                    )}
                  </span>

                  {room.visibility === "private" && isSelectedPrivate && (
                    <div className="join-lobby-screen__private-entry">
                      <input
                        className="join-lobby-screen__private-input"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="ENTER PASSWORD"
                        type="password"
                      />
                      <button
                        className="btn-primary join-lobby-screen__join-btn"
                        onClick={() => onJoin(room, password)}
                        disabled={joining || !password.trim()}
                      >
                        {joining ? "..." : "Join Private Room"}
                      </button>
                    </div>
                  )}
                </div>
              );
            })
          )}
        </div>

        <div className="join-lobby-screen__code-entry">
          <div className="join-lobby-screen__code-row">
            <button className="btn-secondary join-lobby-screen__refresh-btn" onClick={onRefresh} disabled={joining}>
              Refresh Rooms
            </button>
          </div>
          {error && <p className="error-text">{error}</p>}
        </div>
      </div>
    </div>
  );
};

export default JoinLobbyScreen;
