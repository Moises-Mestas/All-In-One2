import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { authService } from "../../services";
import "./login.css";

function Login() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      await authService.login({ email, password });
      navigate("/dashboard");
    } catch (err: any) {
      setError(err.response?.data?.detail || "Error al iniciar sesión");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="layout-page">
      <div className="form-side">
        <div className="card-login">
          <div className="logo-container">
            <img src="" alt="Logo"></img>
          </div>

          {error && <div className="error-message">{error}</div>}

          <form onSubmit={handleSubmit}>
            <div className="form-group">
              {/* 👇 CORRECCIÓN 1: Asociamos el label al input usando htmlFor e id */}
              <label htmlFor="email">Correo electrónico</label>
              <input
                id="email"
                type="email"
                placeholder="ejemplo@correo.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>

            <div className="form-group">
              {/* 👇 CORRECCIÓN 2: Asociamos el label al input usando htmlFor e id */}
              <label htmlFor="password">Contraseña</label>
              <input
                id="password"
                type="password"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>

            <div className="card-footer">
              <button className="btn-login" type="submit" disabled={loading}>
                {loading ? "Iniciando..." : "Iniciar Sesión"}
              </button>

              <p className="link-text">
                ¿Aún no tienes cuenta? <a href="/register">Regístrate</a>
              </p>

              <p className="forgot-password">
                {/* 👇 CORRECCIÓN 3: Cambiamos href="#" por una ruta válida */}
                <a href="/forgot-password">¿Olvidaste tu contraseña?</a>
              </p>
            </div>
          </form>
        </div>
      </div>

      <div className="brand-side">
        <div>
          <h1>All In One</h1>
          <p>Hazlo rápido y fácil</p>
        </div>
      </div>
    </div>
  );
}

export default Login;