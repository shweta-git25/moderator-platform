import { loginUser } from "../services/authService";
import { setToken } from "../utils/tokenService";

export const handleLogin = async (moderator_name, moderator_region_id) => {
  try {
    const response = await loginUser(moderator_name, moderator_region_id);
    if (response.success) {
      setToken(response.data.access_token);
    }

    return response;

  } catch (error) {
    console.error("Login failed:", error);
    throw error;
  }
};
