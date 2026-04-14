import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import "./App.css";
import Login from "./components/login/login";
import Register from "./components/register/register";
import Dashboard from "./pages/dashboard/dashboard";
import SitioWeb from "./pages/sitioWeb/sitioWeb";
import Modulos from "./pages/modulos/modulos";
import WebEditor from "./pages/webEditor/webEditor";
import Plantillas from "./pages/plantillas/plantillas"; 
import BlogManager from './pages/modulos/blog/BlogManager';
import TiendaManager from './pages/modulos/tienda/TiendaManager';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/sitioWeb" element={<SitioWeb />} />
        <Route path="/modulos" element={<Modulos />} />
        <Route path="/webEditor/:siteId" element={<WebEditor />} />
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="/plantillas" element={<Plantillas />} />
        <Route path="/sitioWeb/:siteId/blog" element={<BlogManager />} />
        <Route path="/sitioWeb/:siteId/tienda" element={<TiendaManager />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;