import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";

import LoginPage from "../pages/LoginPage";
import Dashboard from "../pages/Dashboard";
import InfoPage from "../pages/InfoPage";
import PendingEvents from "../pages/PendingEvents";

export const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<LoginPage />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/info" element={<InfoPage />} />
      <Route path="/pending-events/:moderator_id" element={<PendingEvents />} />
      <Route path="*" element={<Navigate to="/" />} />
    </Routes>
  );
};
