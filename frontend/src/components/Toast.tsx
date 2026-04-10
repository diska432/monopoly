import React, { useEffect, useState } from "react";

const Toast: React.FC = () => {
  const [message, setMessage] = useState<string | null>(null);

  useEffect(() => {
    const stored = sessionStorage.getItem("toast");
    if (stored) {
      sessionStorage.removeItem("toast");
      setMessage(stored);
    }
  }, []);

  useEffect(() => {
    if (!message) return;
    const timer = setTimeout(() => setMessage(null), 4000);
    return () => clearTimeout(timer);
  }, [message]);

  if (!message) return null;

  return (
    <div className="toast" onClick={() => setMessage(null)}>
      <span>{message}</span>
    </div>
  );
};

export default Toast;
