import React, { useEffect, useState , useMemo} from "react";
import "../styles/DashboardPage.css";
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-icons/font/bootstrap-icons.css';
import { NotificationBar } from "../components/NotificationBar";
import { useNavigate } from "react-router-dom";
import { fetchEvents, claimEvent, ackEvents, fetchMetrics } from "../controllers/dashboardController";

function DashboardPage() {
  const navigate = useNavigate();
  const [events, setEvents] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [showModal, setShowModal] = useState(false);
  const [claimedEventId, setClaimedEventId] = useState(null);
  const [eventTitle, setEventTitle] =  useState("");
  const [eventDesc, setEventDesc] =  useState("");
  const [eventStats, setEventStats] = useState({ total_events: 0,total_assigned: 0,expired_events: 0});
  const [errors, setErrors] = useState([]);
  

  const pageSize = 10; 
  const storedUser = sessionStorage.getItem("authUser");
  let region_id = ''; let moderator_id=''
  if (storedUser) {
    region_id = JSON.parse(storedUser).region_id;
    moderator_id = (JSON.parse(storedUser).moderator_id)
  }

  const stableRegionId = useMemo(() => region_id, [region_id]);
  const stableModeratorId = useMemo(() => moderator_id, [moderator_id]);

  useEffect(() => {
    if (!region_id) return;

    const loadEvents = async (page) => {
      try {
        const response = await fetchEvents(region_id, page); // make sure your fetchEvents supports page
        setEvents(response.data); // actual event array
        setTotalPages(response.pagination.total_pages);
      } catch (error) {
        console.error(error);
      }
    };

    loadEvents(currentPage);
  }, [region_id, currentPage]);

  useEffect( () => {
    const eventMetricsLoad = async(stableRegionId, stableModeratorId) => {
        try {
          const response = await fetchMetrics(stableRegionId, stableModeratorId); // make sure your fetchEvents supports page
          setEventStats(response.data);
        } catch (error) {
          console.error(error);
        }
    };
    

    eventMetricsLoad(stableRegionId, stableModeratorId);

  },[claimedEventId, stableRegionId, stableModeratorId]);

  const handleLogout = () => {
    localStorage.removeItem("jwtToken");
    navigate("/login");
  };

  const handlePageChange = async (page) => {
    if (page >= 1 && page <= totalPages) {

        setCurrentPage(page);
        
        try {
          const response = await fetchEvents(region_id, page); // use "page" here, NOT currentPage
          setEvents(response.data); // your events array
          setTotalPages(response.pagination.total_pages);
        } catch (error) {
          console.error(error);
        }
      }
    };

    const handleClaimEvent = async (event_id) =>{
      
      try {
        const response = await claimEvent(region_id, event_id, moderator_id); 
        if(response.success){
          setClaimedEventId(response.data.event_id);
          setEventTitle(response.data.event_title);
          setEventDesc(response.data.event_description);
          setShowModal(true);
        }

        if(!response.success) {
          setErrors([response.message]);
          return;
        }

        
      } catch (error) {
        console.error(error);
      }

    }

    const handleAcknowledge = async(event_id) => {
      
      try {
        await ackEvents(event_id, region_id, moderator_id);
        
      } catch (error) {
        console.error("Failed to refresh events:", error);
      }
      setShowModal(false);
    };

    const handleCancel = async () => { 
      setShowModal(false);
      try {
        const response = await fetchEvents(region_id, currentPage);
        setEvents(response.data);           // Update events array
        setTotalPages(response.pagination.total_pages); // Update total pages
      } catch (error) {
        console.error("Failed to refresh events:", error);
      }
    }

    const handlePendingEvents = () => {
      navigate(`/pending-events/${moderator_id}`);
    };

  return (
    <div className="dashboard">
      <div className="d-flex justify-content-between align-items-center p-3 bg-light border-bottom">
        <h1>Dashboard</h1>
        <div className="d-flex align-items-center">
          <span className="me-3">Max</span>
          <i className="bi bi-person-circle fs-3 me-2"></i>
          <button className="btn btn-outline-danger btn-sm" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </div>
      <NotificationBar messages={errors} duration={10000} />
      <div className="metrics">
        <div className="card">
          <h3>Total Events</h3>
          <p>{eventStats.total_events}</p>
        </div>
        <div className="card">
          <h3>Assigned</h3>
          <p>{eventStats.total_assigned}</p>
        </div>
        <div className="card">
          <h3>Expired</h3>
          <p>{eventStats.expired_events}</p>
        </div>
      </div>

      {/* Table */}
      <div className="d-flex justify-content-between align-items-center mb-3">
        <h2 className="mb-0">Events</h2>
        <button className="btn btn-primary" onClick={handlePendingEvents}>
          Pending Events
        </button>
      </div>
      <div className="table-section">
        <div className="container mt-4">

          {events && events.length > 0 ? (
            <>
              <table className="table table-striped table-bordered">
                <thead className="thead-dark">
                  <tr>
                    <th className="text-center">Sr. No.</th>
                    <th className="text-center">Category</th>
                    <th className="text-center">Event</th>
                    <th className="text-center">Action</th>
                  </tr>
                </thead>

                <tbody>
                  {events.map((event, index) => (
                    <tr key={event.event_id}>
                      <td className="text-center">
                        {(currentPage - 1) * pageSize + index + 1}
                      </td>

                      <td className="text-center">{event.category_name}</td>
                      <td className="text-center">{event.event_title}</td>

                      <td className="text-center">
                        <button
                          className={`btn btn-sm me-2 ${
                            claimedEventId === event.event_id
                              ? "btn-warning"
                              : "btn-primary"
                          }`}
                          onClick={() => handleClaimEvent(event.event_id)}
                        >
                          Claim
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>

              {/* Pagination */}
              <nav>
                <ul className="pagination justify-content-center">

                  <li className={`page-item ${currentPage === 1 ? "disabled" : ""}`}>
                    <button
                      className="page-link"
                      onClick={() => handlePageChange(currentPage - 1)}
                    >
                      Previous
                    </button>
                  </li>

                  {Array.from({ length: totalPages }, (_, i) => {
                    const pageNumber = i + 1;
                    return (
                      <li
                        key={pageNumber}
                        className={`page-item ${
                          currentPage === pageNumber ? "active" : ""
                        }`}
                      >
                        <button
                          className="page-link"
                          onClick={() => handlePageChange(pageNumber)}
                        >
                          {pageNumber}
                        </button>
                      </li>
                    );
                  })}

                  <li
                    className={`page-item ${
                      currentPage === totalPages ? "disabled" : ""
                    }`}
                  >
                    <button
                      className="page-link"
                      onClick={() => handlePageChange(currentPage + 1)}
                    >
                      Next
                    </button>
                  </li>

                </ul>
              </nav>
            </>
          ) : (
            <div className="text-center mt-4">
              <h5>No events available</h5>
            </div>
          )}

        </div>
      </div>

      {showModal &&  (
        <div className="modal show d-block" tabIndex="-1">
          <div className="modal-dialog modal-dialog-centered">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title">{eventTitle}</h5>
                <button type="button" className="btn-close" onClick={handleCancel}></button>
              </div>
              <div className="modal-body">
                <p>{eventDesc}</p>
              </div>
              <div className="modal-footer">
                <button type="button" className="btn btn-secondary" onClick={handleCancel}>
                  Cancel
                </button>
                <button type="button" className="btn btn-success ack-btn" onClick={() => handleAcknowledge(claimedEventId)}>
                  Acknowledge
                </button>
              </div>
            </div>
          </div>
        </div>
        )}

      {/* Modal backdrop */}
      {showModal && <div className="modal-backdrop fade show"></div>}

    </div>
  );
}

export default DashboardPage;