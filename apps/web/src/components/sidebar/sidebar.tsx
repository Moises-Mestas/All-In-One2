import "./sidebar.css";
import { authService } from "../../services";
import { useNavigate } from "react-router-dom";

// 👇 CORRECCIÓN: Mini-componente para usar botones reales (<button>) dentro de la lista
// Esto elimina TODOS los errores de accesibilidad de un solo golpe.
const NavItem = ({ icon, text, onClick }: { icon: string; text: string; onClick: () => void }) => (
  <li style={{ padding: 0 }}>
    <button
      onClick={onClick}
      style={{
        background: "transparent",
        border: "none",
        color: "inherit",
        font: "inherit",
        width: "100%",
        padding: "14px 24px",
        display: "flex",
        alignItems: "center",
        gap: "14px",
        cursor: "pointer",
        textAlign: "left",
      }}
    >
      <span className="icon">{icon}</span>
      <span>{text}</span>
    </button>
  </li>
);

function Sidebar() {
  const navigate = useNavigate();

  const handleLogout = () => {
    authService.logout();
    navigate("/login");
  };

  return (
    <div className="sidebar">
      <div className="logo-container">
        <img
          src="https://cdn-icons-png.flaticon.com/512/1005/1005141.png"
          alt="Logo"
          style={{ width: "40px", height: "40px", marginRight: "10px" }}
        />
        <h2>All In One</h2>
      </div>

      <div className="divider"></div>

      {/* 👇 Usamos nuestro nuevo componente NavItem para que el código quede súper limpio */}
      <ul className="nav-menu">
        <NavItem icon="🏠" text="Inicio" onClick={() => navigate("/Dashboard")} />
        <NavItem icon="🌐" text="Sitio Web" onClick={() => navigate("/sitioWeb")} />
        <NavItem icon="📄" text="Plantillas" onClick={() => navigate("/plantillas")} />
        <NavItem icon="📦" text="Módulos" onClick={() => navigate("/modulos")} />
        <NavItem icon="⚙️" text="Configuración" onClick={() => navigate("/configuracion")} />
      </ul>

      <div className="divider"></div>

      <ul className="nav-menu logout-section">
        <NavItem icon="🚪" text="Cerrar Sesión" onClick={handleLogout} />
      </ul>
    </div>
  );
}

export default Sidebar;