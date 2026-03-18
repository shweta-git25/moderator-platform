import axiosInstance from "../api/axiosInstance";
export const getEventsByRegion = async (region_id, page) => {
  try {
    const response = await axiosInstance.get(`/events/${region_id}`,{
      params: { page } });
    return response.data;
  } catch (error) {
    throw error.response?.data || error;
  }
};

export const claimEventByRegion = async(region_id, event_id, moderator_id)=>{
    try {
        const response = await axiosInstance.post(`/claim`, { event_id,  region_id, moderator_id } );
        return response.data;
        
    } catch (error) {
        throw error.response?.data || error;
    }
}

export const ackEventsByRegion = async(event_id, region_id, moderator_id)=>{
    try {
        const response = await axiosInstance.post(`/acknowledge`, { event_id,  region_id, moderator_id } );
        return response.data;
    } catch (error) {
        throw error.response?.data || error;
    }
}

export const  pendingEventsModerator = async(moderator_id) => {
    try {
        const response = await axiosInstance.get(`/ack-pending-events/${moderator_id}`);
        return response.data;
    } catch (error) {
        throw error.response?.data || error;
    }
}

export const eventMetrics = async(region_id, moderator_id) => {
    try {
        const response = await axiosInstance.get(`/event-metrics`, {
      params: { region_id, moderator_id }
    });
        return response.data;
    } catch (error) {
        throw error.response?.data || error;
    }
}