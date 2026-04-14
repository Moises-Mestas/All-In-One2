import React, { useState, useEffect, useRef } from "react";
import axios from "axios";

interface AuthConfig {
  registration_fields: string[];
  custom_fields: Array<{ name: string; label: string }>;
  require_verification: boolean;
}

interface AuthModalProps {
  isOpen: boolean;
  onClose: () => void;
  siteId: number;
  mode: "login" | "register";
}

const API_URL = "http://localhost:8000";

export default function AuthModal({ isOpen, onClose, siteId, mode }: AuthModalProps) {
  const [config, setConfig] = useState<AuthConfig | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [formData, setFormData] = useState<Record<string, string>>({});
  
  // 👇 CORRECCIÓN: Cambiamos el tipo de referencia a HTMLDialogElement
  const backdropRef = useRef<HTMLDialogElement>(null);

  useEffect(() => {
    if (isOpen) {
      setFormData({});
      setError("");
      fetchConfig();
    }
  }, [isOpen, mode]);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };

    const handleBackdropClick = (e: MouseEvent) => {
      if (backdropRef.current && e.target === backdropRef.current) {
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener("keydown", handleKeyDown);
      document.addEventListener("mousedown", handleBackdropClick);
    }

    return () => {
      document.removeEventListener("keydown", handleKeyDown);
      document.removeEventListener("mousedown", handleBackdropClick);
    };
  }, [isOpen, onClose]);

  const fetchConfig = async () => {
    try {
      const { data } = await axios.get(`${API_URL}/api/v1/sites/${siteId}/auth/config`);
      setConfig(data);
    } catch (err) {
      console.error("Error loading auth config:", err);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      if (mode === "register") {
        const customFields: Record<string, string> = {};
        Object.entries(formData)
          .filter(([key]) => key.startsWith("custom_"))
          .forEach(([key, value]) => {
            customFields[key.replace("custom_", "")] = value;
          });

        await axios.post(`${API_URL}/api/v1/sites/${siteId}/auth/register`, {
          email: formData.email,
          password: formData.password,
          first_name: formData.first_name,
          last_name: formData.last_name,
          phone: formData.phone,
          custom_fields: customFields,
        });
      } else {
        await axios.post(`${API_URL}/api/v1/sites/${siteId}/auth/login`, {
          email: formData.email,
          password: formData.password,
        });
      }
      onClose();
    } catch (err: any) {
      setError(err?.response?.data?.detail || "Error en la operación");
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (field: string, value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  if (!isOpen) return null;

  const submitLabel = mode === "login" ? "Iniciar Sesión" : "Crear Cuenta";

  const renderField = (
    fieldName: string,
    label: string,
    type: string = "text",
    required: boolean = false
  ) => (
    <div style={{ marginBottom: "16px" }} key={fieldName}>
      <label style={{ display: "block", marginBottom: "6px", fontWeight: "500", color: "#374151", fontSize: "14px" }}>
        {label} {required && <span style={{ color: "#ef4444" }}>*</span>}
      </label>
      <input
        type={type}
        value={formData[fieldName] || ""}
        onChange={(e) => handleChange(fieldName, e.target.value)}
        required={required}
        style={{
          width: "100%",
          padding: "12px",
          border: "1px solid #d1d5db",
          borderRadius: "8px",
          fontSize: "14px",
          outline: "none",
        }}
      />
    </div>
  );

  return (
    /* 👇 CORRECCIÓN: Usamos la etiqueta nativa <dialog> y agregamos la propiedad 'open'.
          También le quitamos los bordes y márgenes por defecto del navegador */
    <dialog
      ref={backdropRef}
      open
      style={{
        position: "fixed",
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        background: "rgba(0, 0, 0, 0.6)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        zIndex: 99999,
        border: "none",
        padding: 0,
        margin: 0,
        width: "100%",
        height: "100%",
        maxWidth: "100%",
        maxHeight: "100%",
      }}
    >
      <div
        style={{
          background: "white",
          borderRadius: "16px",
          width: "90%",
          maxWidth: "450px",
          overflow: "hidden",
          boxShadow: "0 25px 50px -12px rgba(0, 0, 0, 0.25)",
        }}
      >
        <div
          style={{
            background: mode === "login"
              ? "linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)"
              : "linear-gradient(135deg, #10b981 0%, #059669 100%)",
            padding: "24px",
            color: "white",
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
          }}
        >
          <h2 style={{ margin: 0, fontSize: "20px", fontWeight: "600" }}>
            {submitLabel}
          </h2>
          <button
            onClick={onClose}
            aria-label="Cerrar modal"
            style={{
              background: "rgba(255,255,255,0.2)",
              border: "none",
              color: "white",
              width: "36px",
              height: "36px",
              borderRadius: "8px",
              cursor: "pointer",
              fontSize: "20px",
            }}
          >
            ×
          </button>
        </div>

        <form onSubmit={handleSubmit} style={{ padding: "24px" }}>
          {error && (
            <div
              style={{
                background: "#fef2f2",
                color: "#dc2626",
                padding: "12px",
                borderRadius: "8px",
                marginBottom: "16px",
                fontSize: "14px",
              }}
            >
              {error}
            </div>
          )}

          {mode === "register" && (
            <>
              {renderField("email", "Correo Electrónico", "email", true)}
              {renderField("first_name", "Nombre", "text", false)}
              {renderField("last_name", "Apellido", "text", false)}
              {config?.registration_fields.includes("phone") &&
                renderField("phone", "Teléfono", "tel", false)}

              {config?.custom_fields.map((field) => (
                <div key={field.name} style={{ marginBottom: "16px" }}>
                  <label style={{ display: "block", marginBottom: "6px", fontWeight: "500", color: "#374151", fontSize: "14px" }}>
                    {field.label}
                  </label>
                  <input
                    type="text"
                    value={formData[`custom_${field.name}`] || ""}
                    onChange={(e) => handleChange(`custom_${field.name}`, e.target.value)}
                    style={{
                      width: "100%",
                      padding: "12px",
                      border: "1px solid #d1d5db",
                      borderRadius: "8px",
                      fontSize: "14px",
                      outline: "none",
                    }}
                  />
                </div>
              ))}
            </>
          )}

          {renderField("email", "Correo Electrónico", "email", true)}
          {renderField("password", "Contraseña", "password", true)}

          <button
            type="submit"
            disabled={loading}
            style={{
              width: "100%",
              padding: "14px",
              background: mode === "login" ? "#3b82f6" : "#10b981",
              color: "white",
              border: "none",
              borderRadius: "8px",
              fontSize: "16px",
              fontWeight: "600",
              cursor: loading ? "not-allowed" : "pointer",
              opacity: loading ? 0.7 : 1,
              marginTop: "8px",
            }}
          >
            {loading ? "Procesando..." : submitLabel}
          </button>
        </form>
      </div>
    </dialog>
  );
}