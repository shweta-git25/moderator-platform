import axiosInstance from "./axiosInstance";

// GET
export const getRequest = async (url, params = {}) => {
  try {
    const response = await axiosInstance.get(url, { params });
    return response.data;
  } catch (error) {
    throw error.response?.data || error;
  }
};

// POST
export const postRequest = async (url, data = {}) => {
  try {
    const response = await axiosInstance.post(url, data);
    return response.data;
  } catch (error) {
    throw error.response?.data || error;
  }
};

// PUT
export const putRequest = async (url, data = {}) => {
  try {
    const response = await axiosInstance.put(url, data);
    return response.data;
  } catch (error) {
    throw error.response?.data || error;
  }
};

// DELETE
export const deleteRequest = async (url) => {
  try {
    const response = await axiosInstance.delete(url);
    return response.data;
  } catch (error) {
    throw error.response?.data || error;
  }
};
