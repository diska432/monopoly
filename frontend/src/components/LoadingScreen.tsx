import React from "react";

interface Props {
  message?: string;
}

const LoadingScreen: React.FC<Props> = ({ message = "Loading..." }) => {
  return (
    <div
      className="loading-screen"
      style={{
        backgroundImage: `url(${process.env.PUBLIC_URL}/assets/loading-screen.svg)`,
      }}
    >
      <div className="loading-screen__overlay">
        <div className="loading-screen__content">
          <div className="loading-dots">
            <span className="loading-dot" />
            <span className="loading-dot" />
            <span className="loading-dot" />
          </div>
          <p className="loading-screen__text">{message}</p>
        </div>
      </div>
    </div>
  );
};

export default LoadingScreen;
