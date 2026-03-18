import React, { useEffect, useState } from "react";
import "../styles/InfoPage.css";

function InfoPage({ goToLogin }) {

  const [timeLeft, setTimeLeft] = useState(900); // 15 minutes

  useEffect(() => {

    const timer = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev <= 1) {
          clearInterval(timer);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);

  }, []);

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs < 10 ? "0" : ""}${secs}`;
  };

  return (

    <div className="info-container">

      <div className="info-card">

        <h1>Welcome to Our Platform</h1>

        <p>
          This page provides information before logging into the dashboard.
          You can review the details and continue when ready.
        </p>

        <div className="timer">
          Time Remaining: {formatTime(timeLeft)}
        </div>

        <div className="buttons">

          <button className="primary-btn">
            Continue
          </button>

          <button className="secondary-btn" onClick={goToLogin}>
            Back to Login
          </button>

        </div>

      </div>

    </div>
  );
}

export default InfoPage;
