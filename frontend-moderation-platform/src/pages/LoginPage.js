import React, { useState } from "react";
import "../styles/LoginPage.css";
import { validateLogin } from "../validators/authValidator";
import { handleLogin } from "../controllers/authController";
import { NotificationBar } from "../components/NotificationBar";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/authContext";

function LoginPage() {
  const { login } = useAuth();
  const [moderator_name, setModeratorName] = useState("");
  const [moderator_region_id, setModeratorRegion] = useState(0);
  const [errors, setErrors] = useState([]);
  const navigate = useNavigate();

  const regions = [
    { region_id: 1, region_name: "Asia" },
    { region_id: 2, region_name: "Africa" },
    { region_id: 3, region_name: "Australia" },
    { region_id: 4, region_name: "Europe" },
    { region_id: 5, region_name: "North America" },
    { region_id: 6, region_name: "South America" }
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();

    const validationErrors = validateLogin(moderator_name, moderator_region_id);
    
    if (validationErrors.length > 0) {
      setErrors(validationErrors);
      return;
    }

    try {
      const response = await handleLogin(moderator_name, moderator_region_id);
      
      if(!response.success) {
        setErrors(["Login failed. Please try again."]);
        return;
      }

      login({
        moderator_id: response.data.moderator_id,
        region_id: response.data.region_id,
        token: response.data.access_token,
      });
      
      navigate("/dashboard");



    } catch (err) {
      setErrors(["Login failed. Please try again."]);
    }
  };

  return (
    <div className="login-container">
      <NotificationBar messages={errors} duration={10000} />

      <div className="login-card">
        <h2>Welcome Back</h2>
        <p>Please login to your account</p>

        <form onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Enter User Id"
            value={moderator_name}
            onChange={(e) => setModeratorName(e.target.value)}
          />

          <select
            value={moderator_region_id} onChange={(e) => setModeratorRegion(Number(e.target.value))}>
            <option value="">Please select your Region</option>
            {regions.map((region) => (
              <option key={region.region_id} value={region.region_id}>
                {region.region_name}
              </option>
            ))}
        </select>

          <button type="submit">Login</button>
        </form>
      </div>
    </div>
  );
}

export default LoginPage;
