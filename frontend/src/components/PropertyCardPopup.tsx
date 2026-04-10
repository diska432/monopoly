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
  "Doc-Station",
];

const COLOR_MAP: Record<string, string> = {
  brown: "#765A51", pink: "#FF008C", purple: "#CE72D5", orange: "#D5B772",
  red: "#DC143C", yellow: "#D5B772", green: "#89D572", blue: "#7298D5",
  cyan: "#72CED5",
};

const ERA_MAP: Record<string, string> = {
  brown: "STONE AGE", pink: "CYBERPUNK", purple: "ANCIENT ROME", orange: "MEDIEVAL",
  red: "SOVIET ERA", yellow: "GOLDEN AGE", green: "RENAISSANCE", blue: "INDUSTRIAL",
  cyan: "COSSACK ERA",
};

const PropertyCardPopup: React.FC<Props> = ({ cell, onClose }) => {
  if (!isCompanyCell(cell)) return null;
  const c = cell as CompanyCell;
  const color = COLOR_MAP[c.color] || "#7C6868";
  const era = ERA_MAP[c.color] || c.type.toUpperCase();

  return (
    <div className="prop-popup-overlay" onClick={onClose}>
      <div className="prop-popup" onClick={(e) => e.stopPropagation()}>
        <div className="prop-popup__header" style={{ background: color }}>
          <span className="prop-popup__header-label">WAYPOINT</span>
          <h3 className="prop-popup__header-name">{era}</h3>
        </div>

        <div className="prop-popup__body">
          <h4 className="prop-popup__name">{c.name}</h4>

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
            <div className="prop-popup__stat-row prop-popup__stat-row--highlight">
              <span>Current Rent</span>
              <span>{c.rent} ₸</span>
            </div>
            <div className="prop-popup__stat-row">
              <span>Stars</span>
              <span>{"★".repeat(c.count_stars)}{"☆".repeat(5 - c.count_stars)}</span>
            </div>
            {c.owner_id && (
              <div className="prop-popup__stat-row">
                <span>Owner</span>
                <span className="prop-popup__stat-highlight">{c.owner_id}</span>
              </div>
            )}
            {c.mortgage_count > 0 && (
              <div className="prop-popup__stat-row prop-popup__stat-row--danger">
                <span>Mortgaged</span>
                <span>{c.mortgage_count} turns left</span>
              </div>
            )}
          </div>
        </div>

        <button className="prop-popup__close" onClick={onClose}>CLOSE</button>
      </div>
    </div>
  );
};

export default PropertyCardPopup;
