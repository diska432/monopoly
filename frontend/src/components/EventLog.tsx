import React, { useEffect, useRef } from "react";
import { GameEvent } from "../types/game";

interface Props {
  events: GameEvent[];
}

function formatEvent(e: GameEvent): string {
  switch (e.type) {
    case "dice_rolled": return `🎲 ${e.player} rolled ${e.d1} + ${e.d2} = ${e.d1 + e.d2}`;
    case "moved": return `${e.player} moved to ${e.cell}`;
    case "passed_start": return `${e.player} passed START (+${e.bonus}₸)`;
    case "start_bonus": return `${e.player} landed on START (+${e.bonus}₸)`;
    case "property_bought": return `${e.player} bought ${e.company} for ${e.price}₸`;
    case "buy_declined": return `${e.player} declined to buy ${e.company}`;
    case "rent_paid": return `${e.player} paid ${e.amount}₸ rent to ${e.owner}`;
    case "tax_paid": return `${e.player} paid ${e.amount}₸ tax`;
    case "chance_card": return `🃏 ${e.text} ${e.card_type === "earn" ? `(+${e.amount}₸)` : e.card_type === "pay" ? `(-${e.amount}₸)` : ""}`;
    case "jail": return `🔒 ${e.player} sent to jail: ${e.reason}`;
    case "jail_paid": return `${e.player} paid 50₸ to leave jail`;
    case "doubles": return `${e.player} rolled doubles! (${e.count}x)`;
    case "upgraded": return `${e.player} upgraded ${e.company} to ${e.stars}★`;
    case "star_sold": return `${e.player} sold a star from ${e.company}`;
    case "mortgaged": return `${e.player} mortgaged ${e.company} (+${e.payout}₸)`;
    case "mortgage_lifted": return `${e.player} lifted mortgage on ${e.company}`;
    case "trade_completed": return `Trade completed: ${e.from} ↔ ${e.to}`;
    case "player_resigned": return `${e.player} resigned!`;
    case "game_over": return `🏆 Game Over! Winner: ${e.winner}`;
    case "game_started": return `Game started! ${e.current_player} goes first.`;
    case "player_joined": return `${e.player} joined the game`;
    case "casino_win": return `🎰 ${e.player} won ${e.amount}₸ at the casino!`;
    case "casino_loss": return `🎰 ${e.player} lost at the casino`;
    case "jail_free_doubles": return `${e.player} rolled doubles and escaped jail!`;
    case "jail_expired": return `${e.player} paid 50₸ forced fee after 3 turns in jail`;
    case "jail_stay": return `${e.player} stays in jail (${e.turns_left} turns left)`;
    case "buy_option": return `${e.player} landed on ${e.company} (${e.price}₸)`;
    case "casino_option": return `${e.player} landed on Casino`;
    case "casino_skipped": return `${e.player} skipped the casino`;
    case "auction_started": return `🔨 Auction started for ${e.company}! Starting at ${e.starting_price}₸`;
    case "auction_bid": return `🔨 ${e.player} bids ${e.amount}₸`;
    case "auction_pass": return `${e.player} passes on auction`;
    case "auction_next": return `Next bidder: ${e.current_bidder} (${e.current_price}₸)`;
    case "auction_won": return `🔨 ${e.player} wins auction for ${e.company} at ${e.price}₸!`;
    case "auction_no_winner": return `Auction for ${e.company} ended with no buyers`;
    case "auction_skipped": return `No auction for ${e.company} — no other players`;
    case "error": return `⚠️ ${e.message}`;
    default: return JSON.stringify(e);
  }
}

const EventLog: React.FC<Props> = ({ events }) => {
  const endRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [events.length]);

  const recent = events.slice(-50);

  return (
    <div className="event-log">
      <h4>Game Log</h4>
      <div className="log-entries">
        {recent.map((e, i) => (
          <div key={i} className={`log-entry ${e.type}`}>
            {formatEvent(e)}
          </div>
        ))}
        <div ref={endRef} />
      </div>
    </div>
  );
};

export default EventLog;
