import React, { useState } from "react";
import { GameState, isCompanyCell, CompanyCell } from "../types/game";

interface Props {
  gameState: GameState;
  playerName: string;
  sendAction: (action: string, data?: Record<string, any>) => void;
}

const PlayerPanel: React.FC<Props> = ({ gameState, playerName, sendAction }) => {
  const [showTrade, setShowTrade] = useState(false);
  const [tradeTarget, setTradeTarget] = useState("");
  const [offerCash, setOfferCash] = useState(0);
  const [wantCash, setWantCash] = useState(0);
  const [selectedOffer] = useState<string[]>([]);
  const [selectedWant] = useState<string[]>([]);

  const me = gameState.players.find((p) => p.name === playerName);
  const isMyTurn = gameState.current_player === playerName;
  const pending = gameState.pending_action;
  const pendingPlayer = gameState.pending_player;
  const auction = gameState.auction;

  if (!me) return null;

  const myProperties = gameState.board.filter(
    (c) => isCompanyCell(c) && c.owner_id === playerName
  ) as CompanyCell[];

  const handleTrade = () => {
    sendAction("negotiate", {
      target: tradeTarget,
      offer_cash: offerCash,
      want_cash: wantCash,
      offer_companies: selectedOffer,
      want_companies: selectedWant,
      accepted: true,
    });
    setShowTrade(false);
  };

  const iAmPendingPlayer = pendingPlayer === playerName;
  const iAmAuctionBidder = auction?.current_bidder === playerName;

  return (
    <div className="player-panel">
      <div className="panel-header">
        <h3>{me.name}</h3>
        <span className="balance">{me.balance} ₸</span>
        {me.in_jail_turns > 0 && <span className="jail-badge">In Jail ({me.in_jail_turns})</span>}
      </div>

      {/* Auction UI — shown to the current bidder */}
      {pending === "auction" && auction && (
        <div className="turn-actions">
          {iAmAuctionBidder ? (
            <div className="auction-actions">
              <p className="turn-indicator">Auction: {auction.company}</p>
              <p className="auction-price">Current bid: {auction.current_price} ₸</p>
              {auction.highest_bidder && (
                <p className="auction-leader">Leading: {auction.highest_bidder}</p>
              )}
              <div className="auction-buttons">
                <button className="btn-primary" onClick={() => sendAction("auction_bid")}>
                  Bid {auction.current_price} ₸
                </button>
                <button className="btn-secondary" onClick={() => sendAction("auction_pass")}>
                  Pass
                </button>
              </div>
              <p className="auction-participants">
                Bidders: {auction.participants.join(", ")}
              </p>
            </div>
          ) : auction.participants.includes(playerName) ? (
            <div className="auction-actions">
              <p className="turn-indicator">Auction: {auction.company}</p>
              <p>Waiting for {auction.current_bidder} to bid...</p>
              <p className="auction-price">Current bid: {auction.current_price} ₸</p>
            </div>
          ) : (
            <div className="auction-actions">
              <p className="turn-indicator">Auction: {auction.company}</p>
              <p className="text-muted">You are not in this auction.</p>
            </div>
          )}
        </div>
      )}

      {/* Buy decision — only shown to the pending player */}
      {pending === "buy_decision" && iAmPendingPlayer && (
        <div className="turn-actions">
          <p className="turn-indicator">Buy {gameState.pending_company}?</p>
          <div className="buy-actions">
            <button className="btn-primary" onClick={() => sendAction("buy_property", { accept: true })}>
              Buy
            </button>
            <button className="btn-secondary" onClick={() => sendAction("buy_property", { accept: false })}>
              Pass (Auction)
            </button>
          </div>
        </div>
      )}

      {/* Casino decision — only shown to the pending player */}
      {pending === "casino_decision" && iAmPendingPlayer && (
        <div className="turn-actions">
          <p className="turn-indicator">Casino! (100₸ to play, win 600₸)</p>
          <div className="casino-actions">
            {[1, 2, 3, 4, 5, 6].map((n) => (
              <button key={n} className="btn-dice" onClick={() => sendAction("casino_play", { guess: n })}>
                {n}
              </button>
            ))}
            <button className="btn-secondary" onClick={() => sendAction("casino_skip")}>
              Skip
            </button>
          </div>
        </div>
      )}

      {/* Normal turn actions — roll dice, etc. */}
      {isMyTurn && !pending && (
        <div className="turn-actions">
          <p className="turn-indicator">Your Turn!</p>
          {me.in_jail_turns > 0 ? (
            <div className="jail-actions">
              <button className="btn-primary" onClick={() => sendAction("jail_pay")}>
                Pay 50₸ to Leave Jail
              </button>
              <button className="btn-secondary" onClick={() => sendAction("roll_dice")}>
                Try Rolling Doubles
              </button>
            </div>
          ) : (
            <button className="btn-primary btn-roll" onClick={() => sendAction("roll_dice")}>
              🎲 Roll Dice
            </button>
          )}
        </div>
      )}

      {/* Waiting message if pending action is for someone else */}
      {pending && !iAmPendingPlayer && pending !== "auction" && (
        <div className="turn-actions">
          <p className="text-muted">Waiting for {pendingPlayer}...</p>
        </div>
      )}

      {myProperties.length > 0 && (
        <div className="my-properties">
          <h4>Properties</h4>
          <div className="property-list">
            {myProperties.map((c) => (
              <div key={c.name} className="property-card" style={{ borderTopColor: c.color ? colorHex(c.color) : "#888" }}>
                <span className="prop-name">{c.name}</span>
                <span className="prop-rent">Rent: {c.rent}₸</span>
                {c.count_stars > 0 && <span className="prop-stars">{"★".repeat(c.count_stars)}</span>}
                {c.mortgage_count >= 0 && <span className="mortgaged">Mortgaged</span>}
                {isMyTurn && !pending && (
                  <div className="prop-actions">
                    {c.type === "company" && c.count_stars < 5 && (
                      <button className="btn-tiny" onClick={() => sendAction("upgrade", { company_name: c.name })}>
                        ↑ Star
                      </button>
                    )}
                    {c.count_stars > 0 && (
                      <button className="btn-tiny" onClick={() => sendAction("sell_star", { company_name: c.name })}>
                        ↓ Sell
                      </button>
                    )}
                    {c.mortgage_count < 0 ? (
                      <button className="btn-tiny" onClick={() => sendAction("mortgage", { company_name: c.name })}>
                        Mortgage
                      </button>
                    ) : (
                      <button className="btn-tiny" onClick={() => sendAction("lift_mortgage", { company_name: c.name })}>
                        Lift
                      </button>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {isMyTurn && !pending && (
        <div className="extra-actions">
          <button className="btn-secondary" onClick={() => setShowTrade(!showTrade)}>
            Trade
          </button>
          <button className="btn-danger" onClick={() => sendAction("resign")}>
            Resign
          </button>
        </div>
      )}

      {showTrade && (
        <div className="trade-modal">
          <h4>Trade</h4>
          <label>
            Target Player:
            <select value={tradeTarget} onChange={(e) => setTradeTarget(e.target.value)}>
              <option value="">Select...</option>
              {gameState.players.filter((p) => p.name !== playerName).map((p) => (
                <option key={p.name} value={p.name}>{p.name}</option>
              ))}
            </select>
          </label>
          <label>Offer Cash: <input type="number" value={offerCash} onChange={(e) => setOfferCash(+e.target.value)} /></label>
          <label>Want Cash: <input type="number" value={wantCash} onChange={(e) => setWantCash(+e.target.value)} /></label>
          <button className="btn-primary" onClick={handleTrade}>Send Trade</button>
          <button className="btn-secondary" onClick={() => setShowTrade(false)}>Cancel</button>
        </div>
      )}
    </div>
  );
};

function colorHex(color: string): string {
  const map: Record<string, string> = {
    brown: "#8B4513", pink: "#FF69B4", purple: "#9370DB", orange: "#FF8C00",
    red: "#DC143C", yellow: "#FFD700", green: "#228B22", blue: "#1E90FF",
  };
  return map[color] || "#888";
}

export default PlayerPanel;
