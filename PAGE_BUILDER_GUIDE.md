# Page Builder con Subdominios - Guía de Uso

## Resumen

Se ha implementado un sistema completo de:
- Editor visual con **GrapesJS**
- Subdominios dinámicos para previsualización
- CRUD completo de páginas

## Archivos Creados/Modificados

### Backend (apps/api/app/)
- `models/page.py` - Modelo de página
- `models/component.py` - Modelo de componentes
- `schemas/page.py` - Schemas Pydantic para páginas
- `schemas/component.py` - Schemas para componentes
- `api/pages.py` - Endpoints CRUD de páginas
- `api/public.py` - Endpoints públicos para subdominios
- `middleware/subdomain.py` - Middleware para detectar subdominios
- `main.py` - Actualizado con nuevas rutas

### Frontend (apps/web/src/)
- `types/page.ts` - Tipos TypeScript para páginas
- `services/pages/index.ts` - Servicio API para páginas
- `pages/sitioWeb/editor.tsx` - Editor visual GrapesJS
- `pages/sitioWeb/editor.css` - Estilos del editor
- `App.tsx` - Actualizado con rutas del editor

## Cómo Usar

### 1. Iniciar el Backend
```bash
cd apps/api
uvicorn app.main:app --reload --port 8000
```

### 2. Iniciar el Frontend
```bash
cd apps/web
npm run dev
```

### 3. Crear un Sitio
1. Ve a `http://localhost:5173/sitio-web`
2. Clic en "+ Crear Site"
3. Ingresa nombre y slug (ej: "MiTienda", "mitienda")
4. El sitio estará disponible en: `http://mitienda.localtest.me`

### 4. Usar el Editor
1. Después de crear el sitio, se abre automáticamente el editor
2. Arrastra bloques desde el panel izquierdo
3. Edita estilos en el panel derecho
4. Guarda con "💾 Guardar"
5. Publica con "🚀 Publicar"

## Componentes Disponibles

### Secciones
- **Hero Section** - Header con gradiente y CTA
- **Navbar** - Navegación responsive
- **Features Grid** - Grid de características
- **CTA Section** - Sección de llamado a la acción
- **Footer** - Pie de página

### Básico
- **Texto** - Párrafo editable
- **Imagen** - Placeholder de imagen
- **Botón** - Botón estilizado
- **Divisor** - Línea separadora
- **Columnas** - Grid de 2 columnas

### Interactivo
- **Formulario** - Formulario de contacto
- **Video** - Embed de YouTube

## Estructura de URLs

### Backend API
```
POST   /api/pages                    - Crear página
GET    /api/pages/site/{site_id}     - Listar páginas de un sitio
GET    /api/pages/{page_id}          - Obtener página
PUT    /api/pages/{page_id}          - Actualizar página
DELETE /api/pages/{page_id}          - Eliminar página
POST   /api/pages/{page_id}/save-editor - Guardar desde editor
```

### Sitios Públicos (Subdominios)
```
GET http://{slug}.localtest.me/{page_slug}
```

## Desarrollo Local con Subdominios

### Opción 1: localtest.me (Recomendado)
No requiere configuración. Solo usa el formato:
```
http://mitienda.localtest.me
```

### Opción 2: nip.io
```
http://mitienda.127.0.0.1.nip.io
```

### Opción 3: /etc/hosts (Custom)
Agregar al archivo `/etc/hosts`:
```
127.0.0.1 mitienda.localhost
```

## Producción

Para producción con dominio real:

1. **DNS**: Configurar wildcard DNS
   ```
   *.tudominio.com → IP_DEL_SERVIDOR
   ```

2. **Nginx** como reverse proxy:
   ```nginx
   server {
       listen 80;
       server_name *.tudominio.com;
       
       location / {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
       }
   }
   ```

3. **SSL** con Let's Encrypt:
   ```bash
   certbot --nginx -d *.tudominio.com
   ```

## Próximos Pasos (Opcional)

1. [ ] Agregar más bloques personalizados
2. [ ] Implementar guardado automático
3. [ ] Agregar undo/redo histórico
4. [ ] Integrar sistema de plantillas
5. [ ] Agregar autenticación de usuarios por sitio
6. [ ] Implementar publishing workflow
7. [ ] Agregar analytics básico
8. [ ] Integrar CDN para assets
