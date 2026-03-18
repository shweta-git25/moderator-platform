import React from 'react'
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-icons/font/bootstrap-icons.css';
import { useParams } from "react-router-dom";
import { fetchPendingEvents, ackEvents } from '../controllers/dashboardController';
import { useEffect, useState } from "react";

function PendingEvents() {
    const { moderator_id } = useParams();
    const [events, setEvents] = useState([]);
    const storedUser = sessionStorage.getItem("authUser");
    let region_id = ''; 
    if (storedUser) {
        region_id = JSON.parse(storedUser).region_id;
    }

    useEffect(() => {
        if (!moderator_id) return;
    
        const loadEvents = async (moderator_id) => {
          try {
            const response = await fetchPendingEvents(moderator_id); // make sure your fetchEvents supports page
            setEvents(response.data);
          } catch (error) {
            console.error(error);
          }
        };
    
        loadEvents(moderator_id);
      }, [moderator_id]);

    

    const handleAcknowledge = async(event_id) => {
        console.log("Acknowledging event:", event_id, moderator_id);
        try {
            const response = await ackEvents(event_id, region_id, moderator_id);
            console.log(response);
            
          } catch (error) {
            console.error("Failed to refresh events:", error);
          }
        };
    
    
    
  return (
    <div>
        <div className="d-flex justify-content-between align-items-center mb-3">
        <h2 className="mb-0">Pending Events</h2>
      </div>
      <div className="table-section">
        
        <div className="container mt-4">
          <table className="table table-striped table-bordered">
            <thead className="thead-dark">
              <tr>
                <th className="text-center">Sr. No.</th>
                <th className="text-center">Event</th>
                <th className="text-center">Action</th>
              </tr>
            </thead>
            <tbody>
              {events.map((event, index) => (
                <tr key={event.event_id}>
                  <td className="text-center">{index + 1}</td>
                  <td className="text-center">{event.event_title}</td>
                  <td>
                    <button
                  className={`btn btn-sm me-2 btn-success`}
                  onClick={() => handleAcknowledge(event.event_id)}
                >Acknowledge</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          
        </div>
      </div>

    </div>
  )
}

export default PendingEvents