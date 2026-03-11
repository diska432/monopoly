import React from "react";

interface MainMenuProps {
  displayName: string;
  onStartGame: () => void;
  onLeave: () => void;
}

const MainMenu: React.FC<MainMenuProps> = ({ displayName, onStartGame, onLeave }) => {
  return (
    <div
      className="main-menu"
      style={{ backgroundImage: `url(${process.env.PUBLIC_URL}/assets/bg-campfire.png)` }}
    >
      <div className="main-menu__overlay" />
      <div className="main-menu__content">
        <h1 className="main-menu__title">LEIX IV</h1>

        <nav className="main-menu__nav">
          <button className="main-menu__item main-menu__item--active" onClick={onStartGame}>
            <span className="main-menu__highlight" />
            <span className="main-menu__label">Start Game</span>
          </button>
          <button className="main-menu__item" disabled>
            <span className="main-menu__label">Settings</span>
          </button>
          <button className="main-menu__item" onClick={onLeave}>
            <span className="main-menu__label">Leave</span>
          </button>
        </nav>

        <div className="main-menu__user">
          {displayName}
        </div>
      </div>
    </div>
  );
};

export default MainMenu;
