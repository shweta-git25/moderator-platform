import { getEventsByRegion, claimEventByRegion, ackEventsByRegion, pendingEventsModerator, eventMetrics } from "../services/dashboardService";

export const fetchEvents = async (region_id, page) => {
  try {
    const response = await getEventsByRegion(region_id, page);
    return response;
  } catch (error) {
    console.error("Error fetching events:", error);
    throw error;
  }
};

export const claimEvent = async(region_id, event_id, moderator_id)=>{
    try {
        const response = await claimEventByRegion(region_id, event_id, moderator_id);
        return response;
    } catch (error) {
        console.error("Error claiming events:", error);
        throw error;
    }
}

export const ackEvents = async(event_id,  region_id, moderator_id) => {
    try {
        const response = await ackEventsByRegion(event_id,  region_id, moderator_id);
        return response;
    } catch (error) {
        console.error("Error acknowledging events:", error);
        throw error;
    }
}

export const fetchPendingEvents = async(moderator_id) => {
    try {
        const response = await pendingEventsModerator(moderator_id);
        return response;
    } catch (error) {
        console.error("Error acknowledging events:", error);
        throw error;
    }
}

export const fetchMetrics = async(region_id, moderator_id) => {

    try {
        const response = await eventMetrics(region_id, moderator_id);
        return response;
    } catch (error) {
        console.error("Error fetch metrics events:", error);
        throw error;
    }

}