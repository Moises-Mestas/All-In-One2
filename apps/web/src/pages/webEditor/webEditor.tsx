import grapesjs from "grapesjs";
import "grapesjs/dist/css/grapes.min.css";
import "./webEditor.css";
import { useEffect, useRef, useState } from "react";
import { useParams, useNavigate, useSearchParams } from "react-router-dom";
import { sitesService, SiteAuthService, tiendaService } from "../../services";
import Modal from "../../components/modal/Modal";
import AuthModal from "../../components/auth/AuthModal";
import { getEditorBlocks } from "./editorBlocks"; // 👇 IMPORTAMOS LOS BLOQUES

interface ToastState {
  show: boolean;
  type: "success" | "error" | "info";
  title: string;
  message: string;
}

const smartFormScript = function (this: HTMLElement) {
  const form = this as unknown as HTMLFormElement;
  const handleSubmit = (e: Event) => {
    e.preventDefault();
    const action = form.dataset.action;
    const wa = form.dataset.whatsapp;
    const email = form.dataset.email;

    const nameEl = form.querySelector('[name="name"]') as HTMLInputElement;
    const msgEl = form.querySelector('[name="message"]') as HTMLTextAreaElement;

    const text = "Hola, soy " + (nameEl?.value || "un cliente") + ". " + (msgEl?.value || "");

    if (action === "whatsapp") {
      if (!wa) {
        // @ts-ignore
        if (typeof showToast === 'function') showToast("error", "Configuración Requerida", "Este formulario necesita un número de WhatsApp configurado.");
        return;
      }
      globalThis.open("https://wa.me/" + wa + "?text=" + encodeURIComponent(text), "_blank");
    } else {
      if (!email) {
        // @ts-ignore
        if (typeof showToast === 'function') showToast("error", "Configuración Requerida", "Este formulario necesita un correo configurado.");
        return;
      }
      globalThis.location.href = "mailto:" + email + "?subject=Nuevo Contacto desde la Web&body=" + encodeURIComponent(text);
    }
  };
  form.onsubmit = handleSubmit;
};

const blogListScript = async function (this: any) {
  const container = this.querySelector(".blog-grid-container");
  const siteId = this.dataset.siteId;
  
  if (container && siteId) {
    try {
      const res = await fetch("/modules/blog/" + siteId + "/posts?only_published=true");
      const posts = await res.json();
      
      if (!posts || posts.length === 0) {
        container.innerHTML = '<p style="text-align: center; grid-column: 1 / -1; color: #64748b;">No hay artículos publicados aún.</p>';
        return;
      }
      
      let html = '';
      for (const post of posts) {
        const dateObj = new Date(post.published_at || post.created_at);
        const dateStr = dateObj.toLocaleDateString();
        
        const imgHtml = post.featured_image 
          ? '<img src="' + post.featured_image + '" style="width: 100%; height: 200px; object-fit: cover;" alt="' + post.title + '"/>'
          : '<div style="width: 100%; height: 200px; background: #e2e8f0; display: flex; align-items: center; justify-content: center; color: #94a3b8;">Sin imagen</div>';
        
        html += '<div style="border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; background: white; box-shadow: 0 4px 6px rgba(0,0,0,0.05); transition: transform 0.2s;">' +
                  imgHtml +
                  '<div style="padding: 25px;">' +
                    '<h3 style="margin: 0 0 10px 0; color: #1e293b; font-size: 1.3em;">' + post.title + '</h3>' +
                    '<p style="color: #64748b; line-height: 1.6; margin-bottom: 20px;">' + (post.excerpt || 'Haz clic para leer más...') + '</p>' +
                    '<div style="color: #94a3b8; font-size: 0.9em; font-weight: bold;">📅 ' + dateStr + '</div>' +
                  '</div>' +
                '</div>';
      }
      container.innerHTML = html;
    } catch (err) {
      console.error("Error cargando el blog:", err);
      container.innerHTML = '<p style="text-align: center; color: #ef4444; grid-column: 1 / -1;">Error al cargar las noticias.</p>';
    }
  }
};
  


//hola
function WebEditor() {
  const { siteId } = useParams();
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const editorRef = useRef<any>(null);

  const isTemplate = searchParams.get("isTemplate") === "true";

  const [toast, setToast] = useState<ToastState>({
    show: false,
    type: "info",
    title: "",
    message: "",
  });

  const [authModal, setAuthModal] = useState<{
    show: boolean;
    mode: "login" | "register";
  }>({ show: false, mode: "login" });

  const showToast = (
    type: "success" | "error" | "info",
    title: string,
    message: string,
  ) => {
    setToast({ show: true, type, title, message });
  };

  const hideToast = () => {
    setToast({ ...toast, show: false });
  };

  const openAuthModal = (mode: "login" | "register") => {
    setAuthModal({ show: true, mode });
  };

  const closeAuthModal = () => {
    setAuthModal({ show: false, mode: "login" });
  };

  const renderPagesList = (editor: any, container: any) => {
    container.innerHTML = "";
    const pages = editor.Pages.getAll();

    pages.forEach((page: any) => {
      const pageEl = document.createElement("div");
      pageEl.style.cssText =
        "display: flex; justify-content: space-between; padding: 10px; background: #333; margin-bottom: 5px; border-radius: 3px; cursor: pointer;";

      const nameEl = document.createElement("span");
      nameEl.innerText = page.get("name") || page.id;

      if (editor.Pages.getSelected().id === page.id) {
        nameEl.style.color = "#3498db";
        nameEl.style.fontWeight = "bold";
      }

      const pageId = page.id;
      nameEl.onclick = () => {
        editor.Pages.select(pageId);
        renderPagesList(editor, container);
      };

      pageEl.appendChild(nameEl);
      container.appendChild(pageEl);
    });
  };

  useEffect(() => {
    if (!siteId) return;

    (globalThis as any).siteId = siteId;

    const editor = grapesjs.init({
      container: "#gjs",
      height: "100%",
      width: "auto",

      storageManager: {
        type: "local",
        autosave: false,
        autoload: false,
        id: `gjs-${siteId}-`,
      },
      panels: { defaults: [] },
      deviceManager: {
        devices: [
          { name: "Desktop", width: "" },
          { name: "Mobile", width: "320px", widthMedia: "480px" },
          { name: "Tablet", width: "768px", widthMedia: "992px" },
        ],
      },
      pageManager: {
        pages: [
          {
            id: "page-home",
            name: "Inicio",
            component: "",
          },
        ],
      },
      blockManager: {
        appendTo: "#blocks",
        // 👇 AQUI USAMOS NUESTRO NUEVO ARCHIVO
        blocks: getEditorBlocks(siteId), 
      },
      layerManager: { appendTo: ".layers-container" },
      styleManager: {
        appendTo: ".styles-container",
        sectors: [
          {
            name: "Dimension",
            open: false,
            buildProps: ["width", "min-height", "padding", "margin"],
          },
          {
            name: "Typography",
            open: true,
            buildProps: [
              "font-family",
              "font-size",
              "font-weight",
              "text-align",
              "color",
            ],
          },
          {
            name: "Background",
            open: false,
            buildProps: ["background-color", "background-image"],
          },
          {
            name: "Border",
            open: false,
            buildProps: ["border", "border-radius"],
          },
          {
            name: "Spacing",
            open: false,
            buildProps: ["margin", "padding"],
          },
        ],
      },

      traitManager: { appendTo: ".traits-container" },
      selectorManager: { appendTo: ".styles-container" },
    });

    editorRef.current = editor;

    editor.DomComponents.addType("smart-form", {
      isComponent: (el: any) => {
        if (
          el?.tagName === "FORM" &&
          el?.classList?.contains("smart-form-wa")
        ) {
          return { type: "smart-form" };
        }
      },
      model: {
        defaults: {
          name: "Formulario Inteligente",
          traits: [
            {
              type: "select",
              name: "data-action",
              label: "Enviar a",
              options: [
                {
                  id: "whatsapp",
                  value: "whatsapp",
                  name: "Mensaje de WhatsApp",
                },
                { id: "email", value: "email", name: "Correo Electrónico" },
              ],
            },
            {
              type: "text",
              name: "data-whatsapp",
              label: "N° WhatsApp (Ej: 51999888777)",
            },
            {
              type: "text",
              name: "data-email",
              label: "Tu Correo (Para recibir)",
            },
          ],
          script: smartFormScript,
        },
      },
    });

    editor.DomComponents.addType("blog-list", {
      isComponent: (el: any) => {
        if (el?.dataset?.gjsType === "blog-list") {
          return { type: "blog-list" };
        }
      },
      model: {
        defaults: {
          name: "Módulo Blog",
          script: blogListScript,
        },
      },
    });

    editor.on("component:selected", (component: any) => {
      component.set("resizable", true);
      component.set("hoverable", true);
      component.set("highlightable", true);
    });

    const loadSiteData = async () => {
      try {
        const loadedData = await sitesService.getById(Number(siteId));

        if (loadedData?.settings) {
          editor.loadProjectData(loadedData.settings);
        }
      } catch (error) {
        console.error("Error al cargar el diseño:", error); 
        showToast("error", "Error", "No se pudo cargar el diseño.");
      }
    };

    loadSiteData();

    editor.Panels.addPanel({
      id: "panel-top",
      el: ".panel__top",
    });

    editor.Panels.addPanel({
      id: "basic-actions",
      el: ".panel__basic-actions",
      buttons: [
        {
          id: "visibility",
          active: true,
          className: "btn-toggle-borders",
          label: "B",
          title: "Ver Bordes",
          command: "sw-visibility",
        },

        {
          id: "undo",
          className: "btn-undo",
          label: "↩ Deshacer",
          title: "Deshacer",
          command: (editor: any) => editor.UndoManager.undo(),
        },
        {
          id: "redo",
          className: "btn-redo",
          label: "Rehacer ↪",
          title: "Rehacer",
          command: (editor: any) => editor.UndoManager.redo(),
        },
        {
          id: "save",
          className: "btn-save",
          label: "💾 Guardar",
          title: "Guardar",
          command: "save-db", 
        },
        {
          id: "export",
          className: "btn-open-export",
          label: "<i class='fa fa-code'></i>",
          title: "Ver Código HTML/CSS",
          command: "edit-code",
        },
      ],
    });

    editor.Panels.addPanel({
      id: "panel-devices",
      el: ".panel__devices",
      buttons: [
        {
          id: "device-desktop",
          label: "PC",
          title: "Desktop",
          command: "set-device-desktop",
          active: true,
          togglable: false,
        },
        {
          id: "device-mobile",
          label: "Móvil",
          title: "Mobile",
          command: "set-device-mobile",
          togglable: false,
        },
        {
          id: "device-tablet",
          label: "Tablet",
          title: "Tablet",
          command: "set-device-tablet",
          togglable: false,
        },
      ],
    });

    editor.Panels.addPanel({
      id: "panel-switcher",
      el: ".panel__switcher",
      buttons: [
        { id: "show-blocks", active: true, label: "Bloques", command: "show-blocks", togglable: false },
        { id: "show-layers", active: false, label: "Capas", command: "show-layers", togglable: false },
        { id: "show-style", active: false, label: "Estilos", command: "show-styles", togglable: false },
        { id: "show-traits", active: false, label: "⚙️ Atributos", command: "show-traits", togglable: false },
        { id: "show-pages", active: false, label: "Páginas", command: "show-pages", togglable: false },
      ],
    });

    setTimeout(() => {
      const btnAddPage = document.getElementById("btn-add-page");
      if (btnAddPage) {
        btnAddPage.onclick = () => {
          const pageName = prompt("Nombre de la nueva página (Ej: Contacto):");
          if (pageName) {
            const newPage = editor.Pages.add({
              name: pageName,
              component: "<div><h1>Nueva Página: " + pageName + "</h1></div>",
            });

            if (newPage?.id) {
              editor.Pages.select(String(newPage.id));
              const listContainer = document.getElementById("pages-list");
              if (listContainer) renderPagesList(editor, listContainer);
            }
          }
        };
      }
    }, 1000);

    editor.Commands.add("edit-code", {
      run(editor: any, sender: any) {
        if (sender) sender.set("active", 0);

        let htmlCode = editor.getHtml();
        let cssCode = editor.getCss();

        if (htmlCode) htmlCode = htmlCode.replace(/></g, ">\n<");
        if (cssCode) {
          cssCode = cssCode
            .replace(/}/g, "}\n\n")
            .replace(/{/g, " {\n  ")
            .replace(/;/g, ";\n  ");
        }

        const container = document.createElement("div");

        container.innerHTML = `
          <style>
            .code-editor-area {
              flex: 1;
              background: #1e1e1e;
              color: #d4d4d4;
              font-family: 'Consolas', 'Courier New', monospace;
              padding: 15px;
              border: 1px solid #333;
              border-radius: 5px;
              resize: none;
              font-size: 13px;
              line-height: 1.5;
              outline: none;
              white-space: pre; 
              overflow-x: auto;
            }
            .code-editor-area:focus { border-color: #007acc; }
            .code-label { color: #cccccc; font-weight: 600; margin-bottom: 8px; font-family: sans-serif; font-size: 13px; letter-spacing: 0.5px; }
            .code-btn { padding: 12px 24px; background: #007acc; color: white; border: none; border-radius: 4px; cursor: pointer; font-weight: bold; font-size: 14px; transition: background 0.2s; align-self: flex-end; margin-top: 15px; }
            .code-btn:hover { background: #005f9e; }
            
            .code-editor-area::-webkit-scrollbar { width: 10px; height: 10px; }
            .code-editor-area::-webkit-scrollbar-track { background: #1e1e1e; }
            .code-editor-area::-webkit-scrollbar-thumb { background: #424242; border-radius: 5px; }
            .code-editor-area::-webkit-scrollbar-thumb:hover { background: #4f4f4f; }
          </style>

          <div style="display: flex; flex-direction: column; background: #252526; padding: 20px; border-radius: 8px;">
            <div style="display: flex; gap: 20px; height: 450px;">
              <div style="flex: 1; display: flex; flex-direction: column;">
                <div class="code-label">📝 HTML (Estructura)</div>
                <textarea id="custom-html-code" class="code-editor-area" spellcheck="false"></textarea>
              </div>
              <div style="flex: 1; display: flex; flex-direction: column;">
                <div class="code-label">🎨 CSS (Estilos)</div>
                <textarea id="custom-css-code" class="code-editor-area" spellcheck="false"></textarea>
              </div>
            </div>
            <button id="btn-save-code" class="code-btn">✨ Inyectar Código al Lienzo</button>
          </div>
        `;

        (
          container.querySelector("#custom-html-code") as HTMLTextAreaElement
        ).value = htmlCode || "";
        (
          container.querySelector("#custom-css-code") as HTMLTextAreaElement
        ).value = cssCode || "";

        editor.Modal.setTitle("Editor de Código Avanzado")
          .setContent(container)
          .open();

        const btnSave = container.querySelector(
          "#btn-save-code",
        ) as HTMLButtonElement;
        btnSave.onclick = () => {
          const newHtml = (
            container.querySelector("#custom-html-code") as HTMLTextAreaElement
          ).value;
          const newCss = (
            container.querySelector("#custom-css-code") as HTMLTextAreaElement
          ).value;

          editor.setComponents(newHtml);
          editor.setStyle(newCss);
          editor.Modal.close();
        };
      },
    });

    // 👇 CORRECCIÓN PARA ELIMINAR DUPLICACIONES: Refactorizamos el ocultado de paneles
    const hideAllPanels = (row: any) => {
      ["#blocks", ".layers-container", ".styles-container", ".traits-container", ".pages-container"].forEach(selector => {
        const el = row.querySelector(selector);
        if (el) el.style.display = "none";
      });
    };

    // 👇 CORRECCIÓN PARA ELIMINAR DUPLICACIONES: Unificamos el registro de comandos de paneles
    const registerPanelCommand = (commandId: string, selector: string, isPage?: boolean) => {
      editor.Commands.add(commandId, {
        run(editor: any) {
          const row = editor.getContainer().closest(".editor-row");
          hideAllPanels(row);
          const el = row.querySelector(selector);
          if (el) {
            el.style.display = isPage ? "block" : "";
            if (isPage) renderPagesList(editor, row.querySelector("#pages-list"));
          }
        },
      });
    };

    registerPanelCommand("show-blocks", "#blocks");
    registerPanelCommand("show-layers", ".layers-container");
    registerPanelCommand("show-styles", ".styles-container");
    registerPanelCommand("show-traits", ".traits-container");
    registerPanelCommand("show-pages", ".pages-container", true);

    editor.Commands.add("set-device-desktop", { run: (editor: any) => editor.setDevice("Desktop") });
    editor.Commands.add("set-device-mobile", { run: (editor: any) => editor.setDevice("Mobile") });
    editor.Commands.add("set-device-tablet", { run: (editor: any) => editor.setDevice("Tablet") });

    editor.Commands.add("save-db", {
      async run(editor: any) {
        try {
          const projectData = editor.getProjectData();
          const pagesData: any[] = [];
          const pages = editor.Pages.getAll();

          pages.forEach((page: any) => {
            const component = page.getMainComponent();
            pagesData.push({
              id: page.id,
              name: (page.get("name") || page.id).toLowerCase(),
              html: editor.getHtml({ component }),
              css: editor.getCss({ component }),
            });
          });

          const finalSettings = {
            ...projectData,
            multiPages: pagesData,
            htmlFinal: editor.getHtml(),
            cssFinal: editor.getCss(),
          };

          await sitesService.update(Number(siteId), {
            settings: finalSettings,
          });

          showToast(
            "success",
            "¡Diseño Guardado!",
            isTemplate
              ? "Plantilla maestra actualizada."
              : "Tu sitio web ha sido actualizado.",
          );
        } catch (error) {
          console.error("Error al guardar en la BD:", error);
          showToast("error", "Error al Guardar", "Verifica tu conexión y vuelve a intentarlo.");
        }
      },
    });

    const siteAuth = new SiteAuthService(Number(siteId));

    editor.on("component:add", (model: any) => {
      const btn = model.getEl();
      if (!btn) return;

      if (btn.classList.contains("auth-login-btn")) {
        btn.dataset.authAction = "login";
        btn.onclick = () => openAuthModal("login");
      }

      if (btn.classList.contains("auth-register-btn")) {
        btn.dataset.authAction = "register";
        btn.onclick = () => openAuthModal("register");
      }

      if (btn.classList.contains("auth-logout-btn")) {
        btn.dataset.authAction = "logout";
        
        const handleLogout = async () => {
          if (confirm("¿Cerrar sesión?")) {
            await siteAuth.logout();
            showToast(
              "success",
              "Sesión cerrada",
              "Has cerrado sesión correctamente.",
            );
          }
        };
        btn.onclick = handleLogout;
      }

      if (btn.classList.contains("tienda-agregar-btn")) {
        const productId = btn.dataset.productId;
        
        if (productId) {
          const handleAddToCart = async () => {
            try {
              await tiendaService.agregarAlCarrito(parseInt(productId), 1);
              tiendaService.actualizarUIContador();
              showToast("success", "Agregado", "Producto agregado al carrito");
            } catch (error) {
              console.error("Error al agregar al carrito:", error);
              showToast("error", "Error", "No se pudo agregar al carrito");
            }
          };
          btn.onclick = handleAddToCart;
        } else {
          btn.onclick = () => showToast("info", "Configurar", "Especifica un ID de producto en las propiedades");
        }
      }

      if (btn.classList.contains("tienda-mini-carrito")) {
        btn.onclick = () => {
          const carritoSection = document.querySelector('[data-gjs-type="tienda-carrito"]');
          if (carritoSection) {
            carritoSection.scrollIntoView({ behavior: "smooth" });
          }
        };
        tiendaService.actualizarUIContador();
      }
    });

    return () => {
      if (editor) editor.destroy();
    };
  }, [siteId, isTemplate]);

  return (
    <div className="editor-container">
      <Modal
        isOpen={toast.show}
        onClose={hideToast}
        title={toast.title}
        type={toast.type}
      >
        <p style={{ color: "#374151", fontSize: "15px", lineHeight: "1.6" }}>
          {toast.message}
        </p>
      </Modal>

      <AuthModal
        isOpen={authModal.show}
        onClose={closeAuthModal}
        siteId={Number(siteId)}
        mode={authModal.mode}
      />

      <div className="panel__top">
        <div style={{ display: "flex", alignItems: "center", gap: "0px" }}>
          <button
            style={{
              padding: "8px 15px",
              cursor: "pointer",
              background: "#e74c3c",
              color: "white",
              border: "none",
              borderRadius: "3px",
              fontWeight: "bold",
            }}
            onClick={() => navigate(isTemplate ? "/plantillas" : "/sitioWeb")}
          >
            ⬅ Volver al Gestor
          </button>
          <div className="panel__basic-actions" />
        </div>

        <div className="panel__devices" />
        <div className="panel__switcher" />
      </div>

      <div className="editor-row">
        <div className="editor-canvas">
          <div id="gjs"></div>
        </div>

        <div className="panel__right">
          <div id="blocks" />
          <div className="layers-container" style={{ display: "none" }} />
          <div className="styles-container" style={{ display: "none" }} />
          <div className="traits-container" style={{ display: "none" }} />
          <div
            className="pages-container"
            style={{ display: "none", padding: "10px", color: "#ddd" }}
          >
            <h3 style={{ borderBottom: "1px solid #444", paddingBottom: "10px", marginTop: 0 }}>
              Mis Páginas
            </h3>
            <div id="pages-list"></div>
            <button
              id="btn-add-page"
              style={{
                width: "100%",
                padding: "10px",
                marginTop: "15px",
                background: "#3498db",
                color: "white",
                border: "none",
                borderRadius: "3px",
                cursor: "pointer",
              }}
            >
              + Nueva Página
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default WebEditor;