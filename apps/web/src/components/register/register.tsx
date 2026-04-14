import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { authService } from "../../services";
import "./register.css";

function Register() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    first_name: "",
    last_name: "",
    email: "",
    password: "",
    confirmPassword: "",
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (formData.password !== formData.confirmPassword) {
      setError("Las contraseñas no coinciden");
      return;
    }

    if (formData.password.length < 6) {
      setError("La contraseña debe tener al menos 6 caracteres");
      return;
    }

    setLoading(true);

    try {
      await authService.register({
        email: formData.email,
        password: formData.password,
        first_name: formData.first_name,
        last_name: formData.last_name,
      });
      navigate("/login");
    } catch (err: any) {
      setError(err.response?.data?.detail || "Error al registrarse");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="layout-page">
      <div className="form-side">
        <div className="card-register">
          <div className="logo-container">
            <img src="" alt="Logo"></img>
          </div>

          {error && <div className="error-message">{error}</div>}

          <form onSubmit={handleSubmit}>
            <div className="form-row">
              <div className="form-group">
                {/* 👇 CORRECCIÓN 1: Label vinculado al input */}
                <label htmlFor="first_name">Nombre</label>
                <input
                  id="first_name"
                  type="text"
                  name="first_name"
                  placeholder="Tu nombre"
                  value={formData.first_name}
                  onChange={handleChange}
                  required
                />
              </div>

              <div className="form-group">
                {/* 👇 CORRECCIÓN 2: Label vinculado al input */}
                <label htmlFor="last_name">Apellido</label>
                <input
                  id="last_name"
                  type="text"
                  name="last_name"
                  placeholder="Tu apellido"
                  value={formData.last_name}
                  onChange={handleChange}
                  required
                />
              </div>
            </div>

            <div className="form-group">
              {/* 👇 CORRECCIÓN 3: Label vinculado al input */}
              <label htmlFor="email">Correo electrónico</label>
              <input
                id="email"
                type="email"
                name="email"
                placeholder="ejemplo@correo.com"
                value={formData.email}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-group">
              {/* 👇 CORRECCIÓN 4: Label vinculado al input */}
              <label htmlFor="password">Contraseña</label>
              <input
                id="password"
                type="password"
                name="password"
                placeholder="••••••••"
                value={formData.password}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-group">
              {/* 👇 CORRECCIÓN 5: Label vinculado al input */}
              <label htmlFor="confirmPassword">Confirmar contraseña</label>
              <input
                id="confirmPassword"
                type="password"
                name="confirmPassword"
                placeholder="••••••••"
                value={formData.confirmPassword}
                onChange={handleChange}
                required
              />
            </div>

            <div className="card-footer">
              <button className="btn-register" type="submit" disabled={loading}>
                {loading ? "Creando..." : "Crear Cuenta"}
              </button>

              <p className="link-text">
                ¿Ya tienes cuenta? <a href="/login">Inicia Sesión</a>
              </p>
            </div>
          </form>
        </div>
      </div>

      <div className="brand-side">
        <div>
          <h1>All In One</h1>
          <p>Únete a nuestra comunidad</p>
        </div>
      </div>
    </div>
  );
}

export default Register;