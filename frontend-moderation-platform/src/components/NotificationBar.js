import React, { useEffect, useState } from "react";
import "../styles/Notification.css";

export const NotificationBar = ({ messages = [], duration = 10000 }) => {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    if (messages.length === 0) return;

    setVisible(true);

    const timer = setTimeout(() => {
      setVisible(false);
    }, duration);

    return () => clearTimeout(timer);
  }, [messages, duration]);

  if (!visible || messages.length === 0) return null;

  return (
    <div className="notification-container">
      <div className="notification">
        <ul>
          {messages.map((msg, index) => (
            <li key={index}>{msg}</li>
          ))}
        </ul>
      </div>
    </div>
  );
};
