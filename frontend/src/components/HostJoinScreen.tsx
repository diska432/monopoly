import React from "react";

interface HostJoinScreenProps {
  onHost: () => void;
  onJoin: () => void;
  onBack: () => void;
}

const HostJoinScreen: React.FC<HostJoinScreenProps> = ({ onHost, onJoin, onBack }) => {
  return (
    <div className="host-join">
      <button className="go-back" onClick={onBack}>[ Go Back ]</button>

      <div className="host-join__center">
        <h2 className="host-join__question">Do You Want To?</h2>

        <div className="host-join__choices">
          <button className="host-join__btn host-join__btn--active" onClick={onHost}>
            <span className="host-join__btn-highlight" />
            <span className="host-join__btn-label">Host Game</span>
          </button>
          <button className="host-join__btn" onClick={onJoin}>
            <span className="host-join__btn-label">Join Game</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default HostJoinScreen;
