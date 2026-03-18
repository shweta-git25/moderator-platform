import axiosInstance from "../api/axiosInstance";

export const loginUser = async (moderator_name, moderator_region_id) => {
  try {
    const response = await axiosInstance.post("/login", {
      moderator_name,
      moderator_region_id,
    });

    return response.data;
  } catch (error) {
    throw error.response?.data || error;
  }
};
