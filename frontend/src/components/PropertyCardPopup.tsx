import React from "react";
import { CompanyCell, isCompanyCell, BoardCell } from "../types/game";

interface Props {
  cell: BoardCell;
  onClose: () => void;
}

const RENT_LABELS = [
  "Single Spot",
  "Full Control",
  "With 1 Chip",
  "With 2 Chips",
  "With 3 Chips",
  "With 4 Chips",
];

const COLOR_MAP: Record<string, string> = {
  brown: "#8B4513", pink: "#FF69B4", purple: "#9370DB", orange: "#FF8C00",
  red: "#DC143C", yellow: "#FFD700", green: "#228B22", blue: "#1E90FF",
};

const PropertyCardPopup: React.FC<Props> = ({ cell, onClose }) => {
  if (!isCompanyCell(cell)) return null;
  const c = cell as CompanyCell;
  const color = COLOR_MAP[c.color] || "#888";

  return (
    <div className="prop-popup-overlay" onClick={onClose}>
      <div className="prop-popup" onClick={(e) => e.stopPropagation()}>
        <div className="prop-popup__color-bar" style={{ background: color }} />
        <h3 className="prop-popup__name">{c.name}</h3>
        <p className="prop-popup__type">{c.color?.toUpperCase() || c.type.toUpperCase()}</p>

        <div className="prop-popup__stats">
          <div className="prop-popup__stat-row">
            <span>Price</span>
            <span>{c.price} ₸</span>
          </div>
          {c.type === "company" && (
            <>
              <div className="prop-popup__stat-row">
                <span>{RENT_LABELS[0]}</span>
                <span>{c.initial_rent} ₸</span>
              </div>
              <div className="prop-popup__stat-row">
                <span>Upgrade Cost</span>
                <span>{c.fee} ₸</span>
              </div>
            </>
          )}
          <div className="prop-popup__stat-row">
            <span>Current Rent</span>
            <span className="prop-popup__stat-highlight">{c.rent} ₸</span>
          </div>
          <div className="prop-popup__stat-row">
            <span>Stars</span>
            <span>{"★".repeat(c.count_stars)}{"☆".repeat(5 - c.count_stars)}</span>
          </div>
          {c.owner_id && (
            <div className="prop-popup__stat-row">
              <span>Owner</span>
              <span>{c.owner_id}</span>
            </div>
          )}
          {c.mortgage_count >= 0 && (
            <div className="prop-popup__stat-row prop-popup__stat-row--danger">
              <span>Mortgaged</span>
              <span>{c.mortgage_count} turns left</span>
            </div>
          )}
        </div>

        <button className="prop-popup__close" onClick={onClose}>CLOSE</button>
      </div>
    </div>
  );
};

export default PropertyCardPopup;
