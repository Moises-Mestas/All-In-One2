
const buildColumns = (count: number) => {
  const cols = Array.from({ length: count })
    .map((_, i) => `<div style="flex: 1; min-width: ${count === 3 ? '250' : '200'}px; padding: 15px; background: #f8f9fa; border: 1px dashed #ccc;">Columna ${i + 1}</div>`)
    .join('');
  return `<div style="display: flex; flex-wrap: wrap; gap: ${count === 3 ? '20' : '15'}px; padding: 20px; min-height: 150px;">${cols}</div>`;
};

const buildGalleryImages = () => {
  const urls = [
    "1497366216548-37526070297c", "1504384308090-c894fdcc538d", 
    "1522071820081-009f0129c71c", "1556761175-5973dc0f32d7"
  ];
  return urls.map((id, i) => 
    `<img src="https://images.unsplash.com/photo-${id}?auto=format&fit=crop&w=400&q=80" style="width: 100%; height: 250px; object-fit: cover; border-radius: 8px; transition: transform 0.3s;" alt="Proyecto ${i+1}" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'"/>`
  ).join('');
};

const buildBlogCards = () => {
  const blogs = [
    { img: "1499951360447-b19be8fe80f5", tag: "TECNOLOGÍA", color: "#2563eb", title: "10 Tendencias de diseño para este año", desc: "Descubre las novedades visuales que están dominando el mercado actual...", date: "12 Octubre, 2026" },
    { img: "1553877522-43269d4ea984", tag: "NEGOCIOS", color: "#10b981", title: "Cómo escalar tus ventas usando la web", desc: "Estrategias probadas para aumentar tu tasa de conversión rápidamente...", date: "08 Octubre, 2026" },
    { img: "1522202176988-66273c2fd55f", tag: "EQUIPO", color: "#8b5cf6", title: "Construyendo una cultura empresarial sólida", desc: "El secreto detrás de los equipos altamente productivos y motivados...", date: "01 Octubre, 2026" }
  ];
  
  return blogs.map(b => `
    <div style="border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; transition: transform 0.3s; cursor: pointer;" onmouseover="this.style.transform='translateY(-5px)'" onmouseout="this.style.transform='translateY(0)'">
      <img src="https://images.unsplash.com/photo-${b.img}?auto=format&fit=crop&w=600&q=80" style="width: 100%; height: 200px; object-fit: cover;" alt="${b.title}"/>
      <div style="padding: 25px;">
        <span style="color: ${b.color}; font-weight: bold; font-size: 0.9em;">${b.tag}</span>
        <h3 style="margin: 10px 0; color: #1e293b; font-size: 1.3em;">${b.title}</h3>
        <p style="color: #64748b; line-height: 1.6; margin-bottom: 20px;">${b.desc}</p>
        <div style="color: #94a3b8; font-size: 0.9em;">📅 ${b.date}</div>
      </div>
    </div>`).join('');
};

const buildFeatureCards = () => {
  const features = [
    { icon: "fa-bolt", bg: "#dbeafe", color: "#2563eb", title: "Ultra Rápido", desc: "Infraestructura optimizada para que tus clientes no tengan que esperar ni un milisegundo extra." },
    { icon: "fa-lock", bg: "#d1fae5", color: "#059669", title: "Seguridad Bancaria", desc: "Tus datos y los de tus clientes están protegidos con encriptación de extremo a extremo de grado militar." },
    { icon: "fa-mobile", bg: "#ede9fe", color: "#7c3aed", title: "100% Responsivo", desc: "Se adapta a la perfección a cualquier dispositivo, desde monitores 4K hasta teléfonos móviles pequeños." },
    { icon: "fa-line-chart", bg: "#fef3c7", color: "#d97706", title: "Analítica Integrada", desc: "Mide visitas, clics y conversiones con nuestro panel de métricas sin instalar plugins de terceros." },
    { icon: "fa-paint-brush", bg: "#fce7f3", color: "#db2777", title: "Diseño Personalizable", desc: "Cambia colores, tipografías y formas con un solo clic para que coincida exactamente con tu marca." },
    { icon: "fa-headphones", bg: "#cffafe", color: "#0891b2", title: "Soporte Premium", desc: "Un equipo de expertos disponibles las 24 horas para ayudarte a resolver cualquier duda técnica." }
  ];

  return features.map(f => `
    <div style="padding: 30px; border: 1px solid #e2e8f0; border-radius: 12px; transition: box-shadow 0.3s, border-color 0.3s;" onmouseover="this.style.borderColor='${f.color}'; this.style.boxShadow='0 10px 25px rgba(0,0,0,0.1)'" onmouseout="this.style.borderColor='#e2e8f0'; this.style.boxShadow='none'">
      <div style="width: 50px; height: 50px; background: ${f.bg}; color: ${f.color}; font-size: 24px; border-radius: 10px; display: flex; align-items: center; justify-content: center; margin-bottom: 20px;"><i class="fa ${f.icon}"></i></div>
      <h3 style="font-size: 1.3em; color: #1e293b; margin-bottom: 15px;">${f.title}</h3>
      <p style="color: #64748b; line-height: 1.6; margin: 0;">${f.desc}</p>
    </div>`).join('');
};

const buildFooterLinks = (title: string, links: string[]) => `
  <div>
    <h4 style="color: white; margin-top: 0; margin-bottom: 25px; font-size: 1.1em;">${title}</h4>
    <ul style="list-style: none; padding: 0; margin: 0; line-height: 2.5;">
      ${links.map(l => `<li><a href="#" style="color: #94a3b8; text-decoration: none; transition: color 0.2s;" onmouseover="this.style.color='white'" onmouseout="this.style.color='#94a3b8'">${l}</a></li>`).join('')}
    </ul>
  </div>
`;

// ==========================================
// 🚀 EXPORTACIÓN PRINCIPAL DE BLOQUES
// ==========================================

export const getEditorBlocks = (siteId?: string) => {
  return [
    {
      id: "section",
      label: "<b>Sección Vacía</b>",
      attributes: { class: "fa fa-square-o" },
      content: `<section style="padding: 50px 20px; min-height: 100px;"></section>`,
    },
    {
      id: "blog-dinamico",
      label: "<b>Módulo Blog Real</b>",
      attributes: { class: "fa fa-newspaper-o" },
      content: `
        <section data-gjs-type="blog-posts" style="padding: 40px 20px; background: #f9f9f9;">
          <h2 style="text-align: center;">Últimas Noticias</h2>
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; max-width: 1200px; margin: 0 auto;">
            <div style="padding: 40px; border: 2px dashed #ccc; text-align: center; color: #999;">
              Aquí aparecerán tus noticias publicadas automáticamente.
            </div>
          </div>
        </section>
      `,
    },
    {
      id: "blog-list",
      label: "<b>Lista de Blog</b>",
      attributes: { class: "fa fa-newspaper-o" },
      content: `
        <section data-gjs-type="blog-list" data-site-id="${siteId}" style="padding: 50px 20px; font-family: sans-serif; background: #f8fafc;">
          <h2 style="text-align: center; margin-bottom: 30px; color: #1e293b;">Últimas Noticias</h2>
          <div class="blog-grid-container" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px; max-width: 1200px; margin: 0 auto;">
            <div style="padding: 20px; text-align: center; color: #888; width: 100%;">Cargando artículos dinámicamente...</div>
          </div>
        </section>
      `,
    },
    {
      id: "text",
      label: "Texto",
      attributes: { class: "fa fa-font" },
      content: '<div data-gjs-type="text" style="padding: 10px;">Inserta tu texto aquí...</div>',
    },
    {
      id: "image",
      label: "Imagen",
      attributes: { class: "fa fa-picture-o" },
      select: true,
      content: { type: "image" },
      activate: true,
    },
    {
      id: "3-columns",
      label: "3 Columnas",
      attributes: { class: "fa fa-columns" },
      content: buildColumns(3),
    },
    {
      id: "4-columns",
      label: "4 Columnas",
      attributes: { class: "fa fa-th-large" },
      content: buildColumns(4),
    },
    {
      id: "layout-sidebar-right",
      label: "Contenido + Lateral",
      attributes: { class: "fa fa-columns" },
      content: `<div style="display: flex; flex-wrap: wrap; gap: 30px; padding: 20px; min-height: 200px;">
        <div style="flex: 3; min-width: 300px; padding: 20px; background: #ffffff; border: 1px dashed #ccc;">Contenido Principal (75%)</div>
        <div style="flex: 1; min-width: 250px; padding: 20px; background: #f8f9fa; border: 1px dashed #ccc;">Barra Lateral (25%)</div>
      </div>`,
    },
    {
      id: "heading",
      label: "Título (H2)",
      attributes: { class: "fa fa-header" },
      content: `<h2 style="font-family: sans-serif; color: #333; margin-top: 0; margin-bottom: 15px;">Escribe tu título aquí</h2>`,
    },
    {
      id: "paragraph",
      label: "Párrafo",
      attributes: { class: "fa fa-align-left" },
      content: `<p style="font-family: sans-serif; color: #666; line-height: 1.6; margin-top: 0; margin-bottom: 15px;">Este es un bloque de párrafo. Haz doble clic para editarlo.</p>`,
    },
    {
      id: "link",
      label: "Enlace (Link)",
      attributes: { class: "fa fa-link" },
      content: `<a href="#" style="color: #3498db; text-decoration: none; font-family: sans-serif; font-weight: bold;">Texto del enlace</a>`,
    },
    {
      id: "map",
      label: "Google Maps",
      attributes: { class: "fa fa-map-marker" },
      content: `<div style="padding: 10px; width: 100%;"><iframe width="100%" height="350" frameborder="0" scrolling="no" src="https://maps.google.com/maps?q=Juliaca,Peru&t=&z=13&ie=UTF8&iwloc=&output=embed" style="border-radius: 8px; border: 1px solid #ddd;"></iframe></div>`,
    },
    {
      id: "video",
      label: "Video YouTube",
      attributes: { class: "fa fa-youtube-play" },
      content: `<div style="padding: 10px; width: 100%; display: flex; justify-content: center;"><iframe width="560" height="315" src="https://www.youtube.com/embed/dQw4w9WgXcQ" frameborder="0" style="max-width: 100%; border-radius: 8px;"></iframe></div>`,
    },
    {
      id: "box",
      label: "Caja Libre (Div)",
      attributes: { class: "fa fa-square-o" },
      content: `<div style="min-height: 100px; padding: 20px; border: 1px dashed #ccc; background-color: #f8f9fa; width: 100%; display: block;"></div>`,
    },
    {
      id: "card",
      label: "Tarjeta (Card)",
      attributes: { class: "fa fa-id-card-o" },
      content: `<div style="border: 1px solid #e2e8f0; border-radius: 8px; overflow: hidden; background: white; max-width: 300px; margin: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); display: inline-block;">
        <img src="https://images.unsplash.com/photo-1579546929518-9e396f3cc809?auto=format&fit=crop&w=300&q=80" style="width: 100%; height: 200px; object-fit: cover;" alt="Card image"/>
        <div style="padding: 20px;">
          <h3 style="margin-top: 0; color: #333; font-family: sans-serif;">Título de Tarjeta</h3>
          <p style="color: #666; font-size: 14px; line-height: 1.5; font-family: sans-serif;">Caja ideal para listar servicios o productos.</p>
          <a href="#" style="display: inline-block; padding: 8px 15px; background: #3498db; color: white; text-decoration: none; border-radius: 4px; font-size: 14px;">Leer más</a>
        </div>
      </div>`,
    },
    {
      id: "list",
      label: "Lista de Puntos",
      attributes: { class: "fa fa-list-ul" },
      content: `<ul style="font-family: sans-serif; color: #555; line-height: 1.8; margin-left: 20px;"><li>Primer elemento de la lista</li><li>Segundo elemento importante</li></ul>`,
    },
    {
      id: "icon",
      label: "Ícono Libre",
      attributes: { class: "fa fa-star" },
      content: `<i class="fa fa-star" style="font-size: 32px; color: #f1c40f; display: inline-block; padding: 10px;"></i>`,
    },
    {
      id: "spacer",
      label: "Espaciador",
      attributes: { class: "fa fa-arrows-v" },
      content: `<div style="height: 50px; width: 100%; display: block; clear: both;"></div>`,
    },
    {
      id: "quote",
      label: "Cita (Blockquote)",
      attributes: { class: "fa fa-quote-right" },
      content: `<blockquote style="border-left: 5px solid #3498db; margin: 20px 0; padding: 15px 20px; font-style: italic; color: #555; font-size: 1.2em; font-family: sans-serif; background: #f8f9fa;">"El diseño no es solo lo que se ve y se siente. El diseño es cómo funciona."</blockquote>`,
    },
    {
      id: "badge",
      label: "Etiqueta (Badge)",
      attributes: { class: "fa fa-tag" },
      content: `<span style="display: inline-block; padding: 5px 12px; background-color: #e74c3c; color: white; border-radius: 20px; font-size: 12px; font-weight: bold; font-family: sans-serif;">NUEVO</span>`,
    },
    {
      id: "html-raw",
      label: "Código Libre",
      attributes: { class: "fa fa-code" },
      content: `<div style="padding: 20px; background: #2c3e50; color: #2ecc71; font-family: monospace; text-align: center;"><span>[Widget Personalizado / Código HTML]</span></div>`,
    },
    {
      id: "faq-accordion",
      label: "Preguntas (FAQ)",
      attributes: { class: "fa fa-list" },
      content: `<div style="padding: 40px 20px; max-width: 800px; margin: 0 auto; font-family: sans-serif;">
        <h2 style="text-align: center; margin-bottom: 30px; color: #333;">Preguntas Frecuentes</h2>
        ${["¿Cómo funciona este servicio?", "¿Cuáles son los métodos de pago?"].map(q => `
          <details style="margin-bottom: 10px; border: 1px solid #e2e8f0; border-radius: 5px; padding: 15px; background: #fff;">
            <summary style="font-weight: bold; cursor: pointer; outline: none; color: #2c3e50; font-size: 1.1em;">${q}</summary>
            <p style="margin-top: 15px; color: #666; line-height: 1.5;">Respuesta de ejemplo para tu cliente.</p>
          </details>`).join('')}
      </div>`,
    },
    {
      id: "testimonials",
      label: "Testimonios",
      attributes: { class: "fa fa-comments" },
      content: `<section style="padding: 60px 20px; background: #f8f9fa; font-family: sans-serif; text-align: center;">
        <h2 style="margin-bottom: 40px; color: #333; font-size: 2.5em;">Lo que dicen nuestros clientes</h2>
        <div style="display: flex; flex-wrap: wrap; gap: 30px; justify-content: center; max-width: 1200px; margin: 0 auto;">
          ${[
            { name: "María López", role: "Directora Comercial", quote: "El mejor servicio que he contratado. Completamente recomendado." },
            { name: "Carlos Mendoza", role: "Emprendedor", quote: "Increíble atención al cliente y plataforma sumamente intuitiva." }
          ].map(t => `
            <div style="background: white; padding: 30px; border-radius: 10px; width: 300px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
              <div style="color: #f1c40f; font-size: 24px; margin-bottom: 15px;">★★★★★</div>
              <p style="color: #666; font-style: italic; line-height: 1.6; margin-bottom: 20px;">"${t.quote}"</p>
              <h4 style="margin: 0; color: #333; font-size: 1.2em;">${t.name}</h4><span style="font-size: 14px; color: #999;">${t.role}</span>
            </div>`).join('')}
        </div>
      </section>`,
    },
    {
      id: "team-section",
      label: "Equipo",
      attributes: { class: "fa fa-users" },
      content: `<section style="padding: 60px 20px; font-family: sans-serif; text-align: center;">
        <h2 style="margin-bottom: 40px; color: #333; font-size: 2.5em;">Nuestro Equipo</h2>
        <div style="display: flex; flex-wrap: wrap; gap: 40px; justify-content: center; max-width: 1000px; margin: 0 auto;">
          ${[
            { name: "Roberto Silva", role: "CEO & Fundador", img: "1560250097-0b93528c311a" },
            { name: "Ana Torres", role: "Directora de Tecnología", img: "1573496359142-b8d87734a5a2" }
          ].map(m => `
            <div style="width: 250px;">
              <img src="https://images.unsplash.com/photo-${m.img}?auto=format&fit=crop&w=250&h=250&q=80" style="width: 150px; height: 150px; border-radius: 50%; object-fit: cover; margin-bottom: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);" alt="${m.name}">
              <h3 style="margin: 0 0 5px 0; color: #333;">${m.name}</h3><p style="margin: 0 0 15px 0; color: #3498db; font-weight: bold;">${m.role}</p>
            </div>`).join('')}
        </div>
      </section>`,
    },
    {
      id: "call-to-action",
      label: "Llamado a la Acción",
      attributes: { class: "fa fa-bullhorn" },
      content: `<section style="padding: 60px 20px; background: #3498db; color: white; font-family: sans-serif; text-align: center; border-radius: 8px; margin: 20px;">
        <h2 style="font-size: 2.5em; margin-top: 0; margin-bottom: 15px;">¿Listo para transformar tu negocio?</h2>
        <a href="#" style="display: inline-block; padding: 15px 40px; background: white; color: #3498db; text-decoration: none; border-radius: 30px; font-weight: bold; font-size: 1.1em;">Crear Cuenta Gratis</a>
      </section>`,
    },
    {
      id: "navbar",
      label: "Navegación Simple",
      attributes: { class: "fa fa-bars" },
      content: `<nav style="display: flex; justify-content: space-between; align-items: center; padding: 20px 50px; background: #ffffff; box-shadow: 0 2px 5px rgba(0,0,0,0.1); font-family: sans-serif;">
        <div style="font-weight: bold; font-size: 24px; color: #333;">Mi Empresa</div>
        <div style="display: flex; gap: 30px;">
          ${["Inicio", "Servicios", "Contacto"].map(link => `<a href="#" style="color: #666; text-decoration: none; font-weight: 500;">${link}</a>`).join('')}
        </div>
      </nav>`,
    },
    {
      id: "navbar-responsive",
      label: "Menú Responsivo",
      attributes: { class: "fa fa-bars" },
      content: `
        <style>
          .resp-nav { width: 100%; box-sizing: border-box; display: flex; justify-content: space-between; align-items: center; padding: 15px 30px; background: #ffffff; box-shadow: 0 2px 10px rgba(0,0,0,0.1); font-family: sans-serif; position: relative; z-index: 1000; }
          .resp-nav-brand { font-size: 24px; font-weight: bold; color: #333; text-decoration: none; }
          .nav-toggle-btn { display: none; font-size: 28px; cursor: pointer; color: #333; user-select: none; line-height: 1; padding: 5px; outline: none; }
          .resp-nav-menu { display: flex; gap: 20px; align-items: center; margin: 0; padding: 0; list-style: none; }
          .resp-nav-menu li { position: relative; }
          .resp-nav-menu a { color: #555; text-decoration: none; font-weight: 500; padding: 10px 15px; display: block; transition: color 0.3s; }
          .resp-nav-menu a:hover { color: #3498db; }
          .nav-dropdown-content { display: none; position: absolute; top: 100%; left: 0; background-color: #ffffff; min-width: 220px; box-shadow: 0px 8px 16px rgba(0,0,0,0.1); border-radius: 4px; overflow: hidden; flex-direction: column; z-index: 1001; }
          .nav-dropdown-content a { border-bottom: 1px solid #f0f0f0; padding: 12px 20px; }
          .nav-dropdown-content a:hover { background-color: #f8f9fa; padding-left: 25px; }
          .resp-nav-menu li:hover .nav-dropdown-content { display: flex; }
          .btn-cta { background: #3498db; color: white !important; border-radius: 5px; padding: 10px 20px !important; }
          .btn-cta:hover { background: #2980b9; color: white !important; transform: translateY(-2px); }
          @media (max-width: 768px) {
            .nav-toggle-btn { display: block; }
            .resp-nav-menu { display: none; flex-direction: column; position: absolute; top: 100%; left: 0; width: 100%; background: #ffffff; box-shadow: 0 8px 16px rgba(0,0,0,0.2); padding: 0; align-items: flex-start; border-top: 2px solid #3498db; }
            .resp-nav:focus-within .resp-nav-menu { display: flex; }
            .resp-nav-menu li { width: 100%; border-bottom: 1px solid #eeeeee; }
            .resp-nav-menu a { width: 100%; padding: 18px 30px; box-sizing: border-box; font-size: 16px; }
            .nav-dropdown-content { position: static; box-shadow: none; display: none; background: #f8f9fa; border-left: 4px solid #3498db; margin-left: 0; border-radius: 0;}
            .resp-nav-menu li:hover .nav-dropdown-content { display: flex; }
            .btn-cta { border-radius: 0; background: transparent; color: #3498db !important; font-weight: bold; }
            .btn-cta:hover { background: #eef2f5; transform: none; }
          }
        </style>
        <nav class="resp-nav">
          <a href="#" class="resp-nav-brand">Mi Empresa</a>
          <div class="nav-toggle-btn" tabindex="0">☰</div>
          <ul class="resp-nav-menu">
            <li><a href="#">Inicio</a></li>
            <li><a href="#">Servicios ▾</a>
              <div class="nav-dropdown-content"><a href="#">Opcion 1</a></div>
            </li>
            <li><a href="#" class="btn-cta">Contáctanos</a></li>
          </ul>
        </nav>`,
    },
    {
      id: "hero",
      label: "Hero (Doble clic para imagen)",
      attributes: { class: "fa fa-star" },
      content: `<header style="position: relative; overflow: hidden; padding: 120px 20px; text-align: center; color: white; font-family: sans-serif; min-height: 400px; display: flex; align-items: center; justify-content: center;">
        <img src="https://images.unsplash.com/photo-1556761175-5973dc0f32d7?auto=format&fit=crop&w=1200&q=80" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; z-index: 0;" alt="hero bg" />
        <div style="position: absolute; top:0; left:0; width:100%; height:100%; background: rgba(0,0,0,0.6); z-index: 1;"></div>
        <div style="position: relative; z-index: 2; max-width: 800px; margin: 0 auto;">
          <h1 style="font-size: 3.5em; margin-bottom: 20px; font-weight: bold;">Tu Negocio al Siguiente Nivel</h1>
          <a href="#" style="padding: 15px 30px; background: #3498db; color: white; text-decoration: none; border-radius: 5px; font-weight: bold; font-size: 1.1em;">Empieza Hoy</a>
        </div>
      </header>`,
    },
    {
      id: "carousel",
      label: "Carrusel (Doble clic)",
      attributes: { class: "fa sliders" },
      content: `
        <style>
          .slider-container { width: 100%; overflow: hidden; position: relative; background: #2c3e50; }
          .slider-wrapper { display: flex; width: 300%; animation: slideAnim 15s infinite; }
          .slider-slide { width: 33.333%; height: 500px; position: relative; display: flex; align-items: center; justify-content: center; }
          .slider-bg { position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; z-index: 0; }
          .slider-overlay { position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.4); z-index: 1; pointer-events: none; }
          .slider-content { position: relative; z-index: 2; text-align: center; padding: 20px; color: white; font-family: sans-serif; }
          .slider-content h2 { font-size: 3.5em; margin-bottom: 15px; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); }
          .slider-btn { padding: 15px 30px; background: #e74c3c; color: white; text-decoration: none; border-radius: 5px; font-weight: bold; }
          @keyframes slideAnim {
            0%, 25% { transform: translateX(0); }
            33%, 58% { transform: translateX(-33.3333%); }
            66%, 91% { transform: translateX(-66.6666%); }
            100% { transform: translateX(0); }
          }
        </style>
        <div class="slider-container">
          <div class="slider-wrapper">
            ${[
              { img: "1497366216548-37526070297c", title: "Soluciones Corporativas" },
              { img: "1504384308090-c894fdcc538d", title: "Trabajo en Equipo" },
              { img: "1522071820081-009f0129c71c", title: "Resultados Medibles" }
            ].map(s => `
            <div class="slider-slide">
              <img class="slider-bg" src="https://images.unsplash.com/photo-${s.img}?auto=format&fit=crop&w=1200&q=80" alt="${s.title}"/>
              <div class="slider-overlay"></div>
              <div class="slider-content">
                <h2>${s.title}</h2>
                <a href="#" class="slider-btn">Ver más</a>
              </div>
            </div>`).join('')}
          </div>
        </div>
      `,
    },
    {
      id: "services-grid",
      label: "Grilla de Servicios",
      attributes: { class: "fa fa-th" },
      content: `<section style="padding: 80px 20px; background: #f8f9fa; font-family: sans-serif;">
        <h2 style="text-align: center; margin-bottom: 50px; color: #333; font-size: 2.5em;">Nuestros Servicios</h2>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 30px; max-width: 1200px; margin: 0 auto;">
          ${[
            { icon: "💼", title: "Consultoría" },
            { icon: "🚀", title: "Desarrollo" },
            { icon: "📈", title: "Crecimiento" }
          ].map(s => `
          <div style="background: white; padding: 40px 30px; border-radius: 8px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
            <div style="font-size: 40px; margin-bottom: 20px;">${s.icon}</div>
            <h3 style="color: #333; margin-bottom: 15px;">${s.title}</h3>
          </div>`).join('')}
        </div>
      </section>`,
    },
    {
      id: "pricing",
      label: "Tabla de Precios",
      attributes: { class: "fa fa-money" },
      content: `<section style="padding: 80px 20px; font-family: sans-serif;">
        <h2 style="text-align: center; margin-bottom: 50px; color: #333; font-size: 2.5em;">Planes y Tarifas</h2>
        <div style="display: flex; justify-content: center; gap: 30px; flex-wrap: wrap; max-width: 1000px; margin: 0 auto;">
          <div style="border: 1px solid #e2e8f0; padding: 40px; text-align: center; border-radius: 10px; flex: 1; min-width: 280px;">
            <h3 style="color: #64748b; margin-bottom: 15px; font-size: 1.5em;">Básico</h3>
            <h4 style="font-size: 3em; margin: 20px 0; color: #333;">S/ 99</h4>
            <button style="width: 100%; padding: 15px; background: #f1f5f9; color: #334155; border: none; border-radius: 5px; font-weight: bold; cursor: pointer;">Elegir Plan</button>
          </div>
          <div style="border: 2px solid #3b82f6; padding: 40px; text-align: center; border-radius: 10px; flex: 1; min-width: 280px; transform: scale(1.05); background: white; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);">
            <div style="background: #3b82f6; color: white; padding: 5px 15px; border-radius: 20px; font-size: 0.8em; font-weight: bold; display: inline-block; margin-bottom: 15px;">MÁS POPULAR</div>
            <h3 style="color: #333; margin-bottom: 15px; font-size: 1.5em;">Profesional</h3>
            <h4 style="font-size: 3em; margin: 20px 0; color: #3b82f6;">S/ 199</h4>
            <button style="width: 100%; padding: 15px; background: #3b82f6; color: white; border: none; border-radius: 5px; font-weight: bold; cursor: pointer;">Elegir Plan</button>
          </div>
        </div>
      </section>`,
    },
    {
      id: "smart-contact",
      label: "Formulario Inteligente (WA/Email)",
      attributes: { class: "fa fa-whatsapp" },
      content: `
      <section style="padding: 80px 20px; background: #f8f9fa; font-family: sans-serif;">
        <div style="max-width: 500px; margin: 0 auto; background: white; padding: 40px; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.1);">
          <h2 style="text-align: center; margin-top: 0; color: #2c3e50;">Hablemos</h2>
          <form class="smart-form-wa" data-action="whatsapp" data-whatsapp="51999888777" data-email="tucorreo@empresa.com" style="display: flex; flex-direction: column; gap: 15px; padding: 10px; border: 2px dashed transparent;">
            <input name="name" type="text" placeholder="Tu Nombre" style="padding: 15px; border: 1px solid #e0e6ed; border-radius: 8px; font-size: 16px; width: 100%; box-sizing: border-box;" required/>
            <textarea name="message" rows="4" placeholder="¿En qué podemos ayudarte?" style="padding: 15px; border: 1px solid #e0e6ed; border-radius: 8px; font-size: 16px; width: 100%; box-sizing: border-box; resize: vertical;" required></textarea>
            <button type="submit" style="padding: 15px; background: #25D366; color: white; border: none; border-radius: 8px; font-size: 16px; font-weight: bold; cursor: pointer;">Enviar Mensaje</button>
          </form>
        </div>
      </section>`,
    },
    {
      id: "hero-split",
      label: "Hero Dividido",
      attributes: { class: "fa fa-columns" },
      content: `
      <section style="padding: 80px 20px; background: #ffffff; font-family: sans-serif; overflow: hidden;">
        <div style="display: flex; flex-wrap: wrap; align-items: center; max-width: 1200px; margin: 0 auto; gap: 40px;">
          <div style="flex: 1; min-width: 300px;">
            <span style="display: inline-block; padding: 5px 15px; background: #e0f2fe; color: #0284c7; border-radius: 20px; font-weight: bold; font-size: 14px; margin-bottom: 20px;">🚀 Nueva Actualización</span>
            <h1 style="font-size: 3.5em; color: #1e293b; margin-top: 0; margin-bottom: 20px; line-height: 1.2; font-weight: 800;">Crea cosas increíbles de forma rápida.</h1>
            <a href="#" style="padding: 15px 30px; background: #2563eb; color: white; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 1.1em; transition: background 0.3s;">Comenzar Gratis</a>
          </div>
          <div style="flex: 1; min-width: 300px; text-align: center;">
            <img src="https://images.unsplash.com/photo-1551434678-e076c223a692?auto=format&fit=crop&w=800&q=80" style="width: 100%; max-width: 600px; border-radius: 15px; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);" alt="Dashboard Preview"/>
          </div>
        </div>
      </section>`,
    },
    {
      id: "stats-banner",
      label: "Estadísticas",
      attributes: { class: "fa fa-bar-chart" },
      content: `
      <section style="padding: 60px 20px; background: #2563eb; color: white; font-family: sans-serif;">
        <div style="max-width: 1200px; margin: 0 auto; display: flex; flex-wrap: wrap; justify-content: space-around; gap: 30px; text-align: center;">
          ${[
            { num: "+500", text: "Clientes Felices" },
            { num: "99%", text: "Satisfacción" },
            { num: "24/7", text: "Soporte Técnico" },
            { num: "+10k", text: "Proyectos" }
          ].map(s => `
          <div style="flex: 1; min-width: 150px;">
            <div style="font-size: 3.5em; font-weight: 800; margin-bottom: 10px;">${s.num}</div>
            <div style="font-size: 1.1em; opacity: 0.8; text-transform: uppercase; letter-spacing: 1px;">${s.text}</div>
          </div>`).join('')}
        </div>
      </section>`,
    },
    {
      id: "how-it-works",
      label: "Pasos (Cómo funciona)",
      attributes: { class: "fa fa-step-forward" },
      content: `
      <section style="padding: 80px 20px; background: #f8fafc; font-family: sans-serif;">
        <h2 style="text-align: center; font-size: 2.5em; color: #1e293b; margin-bottom: 60px;">¿Cómo funciona?</h2>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 40px; max-width: 1100px; margin: 0 auto; text-align: center;">
          ${["Regístrate", "Configura", "Publica y Crece"].map((t, i) => `
          <div style="background: white; padding: 40px 20px; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
            <div style="width: 60px; height: 60px; background: #eff6ff; color: #2563eb; font-size: 24px; font-weight: bold; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 20px auto;">${i+1}</div>
            <h3 style="font-size: 1.5em; color: #334155; margin-bottom: 15px;">${t}</h3>
          </div>`).join('')}
        </div>
      </section>`,
    },
    {
      id: "blog-grid",
      label: "Grilla de Artículos",
      attributes: { class: "fa fa-newspaper-o" },
      content: `
      <section style="padding: 80px 20px; background: #ffffff; font-family: sans-serif;">
        <div style="max-width: 1200px; margin: 0 auto;">
          <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 50px; flex-wrap: wrap; gap: 20px;">
            <div>
              <h2 style="font-size: 2.5em; color: #1e293b; margin: 0 0 10px 0;">Últimas Novedades</h2>
            </div>
            <a href="#" style="padding: 10px 20px; border: 2px solid #e2e8f0; color: #475569; text-decoration: none; border-radius: 6px; font-weight: bold;">Ver todos</a>
          </div>
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px;">
            ${buildBlogCards()}
          </div>
        </div>
      </section>`,
    },
    {
      id: "image-gallery",
      label: "Galería de Proyectos",
      attributes: { class: "fa fa-th" },
      content: `
      <section style="padding: 60px 20px; text-align: center; font-family: sans-serif;">
        <h2 style="font-size: 2.5em; color: #333; margin-bottom: 40px;">Nuestros Trabajos</h2>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; max-width: 1200px; margin: 0 auto;">
          ${buildGalleryImages()}
        </div>
      </section>`,
    },
    {
      id: "features-zigzag",
      label: "Bloques Alternados",
      attributes: { class: "fa fa-exchange" },
      content: `
      <section style="padding: 60px 20px; font-family: sans-serif; overflow: hidden;">
        <div style="display: flex; flex-wrap: wrap; align-items: center; max-width: 1100px; margin: 0 auto 60px auto; gap: 40px;">
          <div style="flex: 1; min-width: 300px;">
            <h2 style="font-size: 2.2em; color: #2c3e50; margin-bottom: 20px;">Diseño Enfocado en Resultados</h2>
            <a href="#" style="color: #3498db; text-decoration: none; font-weight: bold; font-size: 1.1em;">Conocer más →</a>
          </div>
          <div style="flex: 1; min-width: 300px;">
            <img src="https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=600&q=80" style="width: 100%; border-radius: 12px; box-shadow: 0 20px 40px rgba(0,0,0,0.1);" alt="Feature 1"/>
          </div>
        </div>
        <div style="display: flex; flex-wrap: wrap-reverse; align-items: center; max-width: 1100px; margin: 0 auto; gap: 40px;">
          <div style="flex: 1; min-width: 300px;">
            <img src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=600&q=80" style="width: 100%; border-radius: 12px; box-shadow: 0 20px 40px rgba(0,0,0,0.1);" alt="Feature 2"/>
          </div>
          <div style="flex: 1; min-width: 300px;">
            <h2 style="font-size: 2.2em; color: #2c3e50; margin-bottom: 20px;">Analítica Avanzada</h2>
            <a href="#" style="color: #3498db; text-decoration: none; font-weight: bold; font-size: 1.1em;">Ver estadísticas →</a>
          </div>
        </div>
      </section>`,
    },
    {
      id: "footer",
      label: "Pie de Página",
      attributes: { class: "fa fa-long-arrow-down" },
      content: `<footer style="padding: 60px 20px 20px 20px; background: #1e293b; color: #94a3b8; font-family: sans-serif;">
        <div style="max-width: 1200px; margin: 0 auto; display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 40px; margin-bottom: 40px;">
          <div><h3 style="color: white; margin-bottom: 20px; font-size: 1.5em;">Mi Empresa</h3></div>
          <div><h4 style="color: white; margin-bottom: 20px;">Enlaces Rápidos</h4></div>
          <div><h4 style="color: white; margin-bottom: 20px;">Contacto</h4><p>✉️ hola@miempresa.com</p></div>
        </div>
      </footer>`,
    },
    {
      id: "columns",
      label: "2 Columnas",
      attributes: { class: "fa fa-columns" },
      content: buildColumns(2),
    },
    {
      id: "button",
      label: "Botón Simple",
      attributes: { class: "fa fa-square" },
      content: '<a href="#" style="display: inline-block; padding: 12px 24px; background: #000; color: #fff; text-decoration: none; border-radius: 4px; text-align: center;">Haz clic aquí</a>',
    },
    {
      id: "divider",
      label: "Separador",
      attributes: { class: "fa fa-minus" },
      content: '<hr style="margin: 40px 0; border: none; border-top: 1px solid #e2e8f0;">',
    },
    {
      id: "hero-saas",
      label: "Hero SaaS Avanzado",
      attributes: { class: "fa fa-rocket" },
      content: `
      <section style="padding: 100px 20px 60px 20px; background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%); font-family: sans-serif; text-align: center; overflow: hidden;">
        <div style="max-width: 900px; margin: 0 auto; position: relative; z-index: 2;">
          <h1 style="font-size: 4em; color: #0f172a; margin-top: 0; margin-bottom: 25px; line-height: 1.1; font-weight: 900; letter-spacing: -1px;">El software que tu equipo <span style="color: #3b82f6;">amará usar.</span></h1>
          <div style="display: flex; gap: 20px; justify-content: center; margin-bottom: 60px;">
            <a href="#" style="padding: 16px 35px; background: #0f172a; color: white; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 1.1em;">Prueba Gratis por 14 días</a>
          </div>
        </div>
      </section>`,
    },
    {
      id: "features-6-grid",
      label: "Grilla de 6 Beneficios",
      attributes: { class: "fa fa-th-large" },
      content: `
      <section style="padding: 100px 20px; background: #ffffff; font-family: sans-serif;">
        <div style="text-align: center; max-width: 800px; margin: 0 auto 60px auto;">
          <h2 style="font-size: 2.8em; color: #1e293b; margin-bottom: 20px;">Todo lo que necesitas para triunfar</h2>
        </div>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px; max-width: 1200px; margin: 0 auto;">
          ${buildFeatureCards()}
        </div>
      </section>`,
    },
    {
      id: "trust-brands",
      label: "Marcas que confían",
      attributes: { class: "fa fa-handshake-o" },
      content: `
      <section style="padding: 50px 20px; background: #f8fafc; text-align: center; border-top: 1px solid #e2e8f0; border-bottom: 1px solid #e2e8f0;">
        <div style="display: flex; flex-wrap: wrap; justify-content: center; align-items: center; gap: 40px; max-width: 1000px; margin: 0 auto; opacity: 0.5; filter: grayscale(100%);">
          ${["amazon", "google", "apple", "spotify", "paypal", "slack"].map(b => `<i class="fa fa-${b}" style="font-size: 40px; color: #333;"></i>`).join('')}
        </div>
      </section>`,
    },
    {
      id: "faq-modern",
      label: "FAQ Avanzado (Lateral)",
      attributes: { class: "fa fa-question-circle" },
      content: `
      <section style="padding: 100px 20px; background: #ffffff; font-family: sans-serif;">
        <div style="max-width: 1200px; margin: 0 auto; display: flex; flex-wrap: wrap; gap: 50px;">
          <div style="flex: 1; min-width: 300px;">
            <h2 style="font-size: 3em; color: #0f172a; margin-top: 0; margin-bottom: 20px; line-height: 1.1; font-weight: 800;">Preguntas<br>Frecuentes</h2>
          </div>
          <div style="flex: 2; min-width: 300px; display: flex; flex-direction: column; gap: 15px;">
            ${Array(4).fill(0).map(() => `
            <details style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 20px; cursor: pointer;">
              <summary style="font-weight: bold; font-size: 1.1em; color: #1e293b; outline: none; list-style-position: inside;">¿Pregunta de ejemplo?</summary>
              <p style="color: #64748b; margin-top: 15px; margin-bottom: 0; line-height: 1.6;">Respuesta de ejemplo.</p>
            </details>`).join('')}
          </div>
        </div>
      </section>`,
    },
    {
      id: "footer-mega",
      label: "Footer Completo + Newsletter",
      attributes: { class: "fa fa-sitemap" },
      content: `
      <footer style="background: #0f172a; color: #cbd5e1; font-family: sans-serif; padding-top: 80px;">
        <div style="max-width: 1200px; margin: 0 auto; padding: 0 20px; display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 40px; border-bottom: 1px solid #1e293b; padding-bottom: 60px;">
          <div style="grid-column: span 2; min-width: 300px;">
            <h3 style="color: white; font-size: 1.8em; margin-top: 0; margin-bottom: 20px;">MiEmpresa<span style="color: #3b82f6;">.</span></h3>
          </div>
          ${buildFooterLinks("Producto", ["Características", "Integraciones", "Tarifas", "Registro de Cambios"])}
          ${buildFooterLinks("Compañía", ["Sobre Nosotros", "Trabaja Aquí", "Blog", "Contacto"])}
          ${buildFooterLinks("Legal", ["Política de Privacidad", "Términos de Servicio", "Cookies"])}
        </div>
      </footer>`,
    },
    {
      id: "auth-login-btn",
      label: "Botón Login",
      attributes: { class: "fa fa-sign-in" },
      content: `<button class="auth-login-btn" style="padding: 12px 24px; background: #3b82f6; color: white; border: none; border-radius: 8px; cursor: pointer; font-size: 14px; font-weight: 600;">Iniciar Sesión</button>`,
    },
    {
      id: "auth-register-btn",
      label: "Botón Registro",
      attributes: { class: "fa fa-user-plus" },
      content: `<button class="auth-register-btn" style="padding: 12px 24px; background: #10b981; color: white; border: none; border-radius: 8px; cursor: pointer; font-size: 14px; font-weight: 600;">Registrarse</button>`,
    },
    {
      id: "auth-user-info",
      label: "Info Usuario",
      attributes: { class: "fa fa-user-circle" },
      content: `<div class="auth-user-info" style="display: flex; align-items: center; gap: 12px; padding: 10px 16px; background: #f1f5f9; border-radius: 8px;">
        <span style="font-weight: 600; color: #334155;">¡Hola, Usuario!</span>
        <button class="auth-logout-btn" style="padding: 6px 12px; background: #ef4444; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 12px;">Cerrar Sesión</button>
      </div>`,
    },
    {
      id: "tienda-producto-card",
      label: "Card Producto",
      attributes: { class: "fa fa-shopping-bag" },
      content: `
        <div class="tienda-producto-card" data-gjs-type="tienda-producto-card" style="border: 1px solid #e5e7eb; border-radius: 12px; overflow: hidden; max-width: 300px; background: white;">
          <div class="producto-imagen" style="height: 200px; background: #f3f4f6; display: flex; align-items: center; justify-content: center;"><span style="color: #9ca3af; font-size: 40px;">📦</span></div>
          <div style="padding: 16px;">
            <div class="producto-nombre" style="font-size: 16px; font-weight: 600; color: #1f2937; margin-bottom: 8px;">Automático</div>
            <div class="producto-precio" style="font-size: 20px; font-weight: 700; color: #059669; margin-bottom: 12px;">S/ 0.00</div>
            <button class="tienda-agregar-btn" data-product-id="" style="width: 100%; padding: 10px; background: #3b82f6; color: white; border: none; border-radius: 8px; font-weight: 600; cursor: pointer;">Agregar al Carrito</button>
          </div>
        </div>
      `,
    },
    {
      id: "tienda-productos-grilla",
      label: "Grilla Productos",
      attributes: { class: "fa fa-th-large" },
      content: `
        <section data-gjs-type="tienda-productos" style="padding: 40px 20px; background: #ffffff;">
          <div style="max-width: 1200px; margin: 0 auto;">
            <h2 style="text-align: center; margin-bottom: 30px; color: #1f2937;">Nuestros Productos</h2>
            <div class="tienda-productos-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 24px;"></div>
          </div>
        </section>
      `,
    },
    {
      id: "tienda-producto-destacado",
      label: "Producto Destacado",
      attributes: { class: "fa fa-star" },
      content: `
        <section data-gjs-type="tienda-producto-destacado" style="padding: 60px 20px; background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);">
          <div style="max-width: 1000px; margin: 0 auto; display: flex; flex-wrap: wrap; align-items: center; gap: 40px;">
            <div style="flex: 1; min-width: 300px;">
              <span style="display: inline-block; padding: 4px 12px; background: #f59e0b; color: white; border-radius: 20px; font-size: 12px; font-weight: 600; margin-bottom: 16px;">PRODUCTO DESTACADO</span>
              <h2 style="font-size: 2.5em; color: #1f2937; margin: 0 0 16px 0;">Nombre del Producto</h2>
              <button class="tienda-agregar-btn" data-product-id="" style="padding: 14px 32px; background: #3b82f6; color: white; border: none; border-radius: 8px; font-size: 16px; font-weight: 600; cursor: pointer;">Agregar al Carrito</button>
            </div>
          </div>
        </section>
      `,
    },
    {
      id: "tienda-mini-carrito",
      label: "Mini Carrito",
      attributes: { class: "fa fa-shopping-cart" },
      content: `
        <div class="tienda-mini-carrito" style="position: fixed; bottom: 20px; right: 20px; z-index: 1000; cursor: pointer;">
          <div style="background: #3b82f6; color: white; padding: 16px 24px; border-radius: 50px; box-shadow: 0 4px 20px rgba(59, 130, 246, 0.4); display: flex; align-items: center; gap: 12px;">
            <span style="font-size: 20px;">🛒</span>
            <span class="carrito-contador" style="font-weight: 700;">0</span>
          </div>
        </div>
      `,
    },
    {
      id: "tienda-carrito-page",
      label: "Carrito de Compras",
      attributes: { class: "fa fa-cart-arrow-down" },
      content: `
        <section data-gjs-type="tienda-carrito" style="padding: 60px 20px; background: #f9fafb; min-height: 400px;">
          <div style="max-width: 1000px; margin: 0 auto;">
            <h2 style="text-align: center; margin-bottom: 40px; color: #1f2937;">Carrito de Compras</h2>
            <div class="tienda-carrito-items" style="background: white; border-radius: 12px; padding: 24px; margin-bottom: 24px;"></div>
          </div>
        </section>
      `,
    },
    {
      id: "tienda-checkout",
      label: "Checkout",
      attributes: { class: "fa fa-credit-card" },
      content: `
        <section data-gjs-type="tienda-checkout" style="padding: 60px 20px; background: #f9fafb;">
          <div style="max-width: 800px; margin: 0 auto;">
            <h2 style="text-align: center; margin-bottom: 40px; color: #1f2937;">Finalizar Compra</h2>
          </div>
        </section>
      `,
    },
    {
      id: "tienda-categorias-menu",
      label: "Menú Categorías",
      attributes: { class: "fa fa-folder" },
      content: `
        <nav class="tienda-categorias-menu" style="padding: 16px 20px; background: #ffffff; border-bottom: 1px solid #e5e7eb;">
          <ul style="display: flex; gap: 24px; list-style: none; margin: 0; padding: 0; flex-wrap: wrap; justify-content: center;">
            ${["Todos", "Categoría 1", "Categoría 2", "Categoría 3"].map((c, i) => `<li><a href="#" style="color: ${i === 0 ? '#3b82f6' : '#4b5563'}; font-weight: ${i === 0 ? '600' : 'normal'}; text-decoration: none;">${c}</a></li>`).join('')}
          </ul>
        </nav>
      `,
    },
  ];
};