import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Sidebar from "../../components/sidebar/sidebar";
import { authService, sitesService } from "../../services";
import type { Site } from "../../types";
import "./dashboard.css";

function Dashboard() {
  const navigate = useNavigate();
  const [user, setUser] = useState<any>(null);
  const [sites, setSites] = useState<Site[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      navigate("/login");
      return;
    }
    loadData();
  }, [navigate]);

  const loadData = async () => {
    try {
      const userData = await authService.getMe();
      setUser(userData);

      const sitesData = await sitesService.getAll();
      setSites(sitesData);
    } catch (err) {
      console.error("Error loading data:", err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Cargando...</div>;
  }

  return (
    <div className="dashboard-container">
      <Sidebar />
      <div className="main-content">
        <div>
          <h1>Bienvenido, {user?.first_name}</h1>
          <p className="user-email">{user?.email}</p>
        </div>
        <div>
          <ul>
            {sites.map((site) => (
              <li key={site.id}>{site.name}</li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
