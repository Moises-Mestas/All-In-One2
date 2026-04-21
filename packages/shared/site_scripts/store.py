import json
from typing import List, Dict, Any


def get_store_card_script(site_id: int) -> str:
    script = f'''<script>
(function() {{
    var siteId = {site_id};
    var API = '/api/v1/sites/' + siteId + '/tienda';

    function getProductos() {{
        return fetch(API + '/productos?solo_activos=true')
        .then(function(r) {{ return r.json(); }})
        .then(function(data) {{ return data.data || data.productos || []; }})
        .catch(function() {{ return []; }});
    }}

    function getUserData() {{
        var token = localStorage.getItem('site_' + siteId + '_token');
        var userStr = localStorage.getItem('site_' + siteId + '_user');
        if (token && userStr) {{
            try {{ return JSON.parse(userStr); }} catch(e) {{ return null; }}
        }}
        return null;
    }}

    function getAuthToken() {{
        return localStorage.getItem('site_' + siteId + '_token');
    }}

    function getAuthHeaders() {{
        var token = getAuthToken();
        if (token) {{
            return {{ 'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json' }};
        }}
        return {{ 'Content-Type': 'application/json' }};
    }}

    function getCarrito() {{
        var user = getUserData();
        if (!user || !user.id) return Promise.resolve({{ id: 0, items: [], total: 0 }});
        
        var headers = getAuthHeaders();
        return fetch(API + '/carrito?usuario_id=' + user.id, {{ method: 'GET', headers: headers }})
        .then(function(r) {{ return r.json(); }})
        .catch(function() {{ return {{ id: 0, items: [], total: 0 }}; }});
    }}

    function buildCard(producto) {{
        var imagen = '';
        if (producto.imagenes && producto.imagenes.length > 0) {{
            imagen = '<div class="producto-imagen" style="height:200px;background-image:url(' + producto.imagenes[0] + ');background-size:cover;background-position:center;"></div>';
        }} else {{
            imagen = '<div class="producto-imagen" style="height:200px;background:#f3f4f6;display:flex;align-items:center;justify-content:center;"><span style="color:#9ca3af;font-size:40px;">📦</span></div>';
        }}

        var descripcion = producto.descripcion || '';
        if (descripcion.length > 100) descripcion = descripcion.substring(0, 100) + '...';
        var descHtml = descripcion ? '<div class="producto-descripcion" style="font-size:14px;color:#6b7280;margin-bottom:12px;line-height:1.5;">' + descripcion + '</div>' : '';

        var precio = parseFloat(producto.precio || 0).toFixed(2);
        var precioHtml = '<span class="producto-precio" style="font-size:20px;font-weight:700;color:#059669;">S/ ' + precio + '</span>';

        if (producto.precio_comparacion && parseFloat(producto.precio_comparacion) > parseFloat(producto.precio)) {{
            precioHtml += '<span style="font-size:14px;color:#9ca3af;text-decoration:line-through;margin-left:8px;">S/ ' + parseFloat(producto.precio_comparacion).toFixed(2) + '</span>';
        }}

        var stockHtml = '';
        if (producto.stock !== undefined && producto.stock !== null) {{
            if (producto.stock > 0) {{
                stockHtml = '<div style="font-size:13px;color:#10b981;margin-bottom:12px;">Stock: ' + producto.stock + '</div>';
            }} else {{
                stockHtml = '<div style="font-size:13px;color:#dc2626;margin-bottom:12px;">Sin stock</div>';
            }}
        }}

        var btnDisabled = (producto.stock == 0) ? 'disabled style="opacity:0.5;cursor:not-allowed;"' : '';
        var btnHtml = '<button class="tienda-agregar-btn" data-product-id="' + producto.id + '" ' + btnDisabled + ' style="width:100%;padding:10px;background:#3b82f6;color:white;border:none;border-radius:8px;font-weight:600;cursor:pointer;">Agregar al Carrito</button>';

        return '<div class="tienda-producto-card" data-product-id="' + producto.id + '" style="border: 1px solid #e5e7eb; border-radius: 12px; overflow: hidden; max-width: 300px; background: white;">' +
            imagen +
            '<div style="padding:16px;">' +
                '<div class="producto-nombre" style="font-size:16px;font-weight:600;color:#1f2937;margin-bottom:8px;">' + producto.nombre + '</div>' +
                descHtml +
                '<div style="margin-bottom:12px;">' + precioHtml + '</div>' +
                stockHtml +
                btnHtml +
            '</div>' +
        '</div>';
    }}

    function buildGrilla(productos) {{
        var html = '';
        productos.forEach(function(producto) {{
            html += buildCard(producto);
        }});
        return html;
    }}

    function buildDestacado(producto) {{
        var imagen = '';
        if (producto.imagenes && producto.imagenes.length > 0) {{
            imagen = '<img src="' + producto.imagenes[0] + '" style="width: 100%; height: 300px; object-fit: cover; border-radius: 12px 12px 0 0;">';
        }} else {{
            imagen = '<div style="height: 300px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); display: flex; align-items: center; justify-content: center; border-radius: 12px 12px 0 0;"><span style="font-size: 80px;">📦</span></div>';
        }}

        var precio = parseFloat(producto.precio || 0).toFixed(2);
        var precioHtml = '<span style="font-size: 28px; font-weight: 700; color: #059669;">S/ ' + precio + '</span>';

        return '<div class="tienda-producto-destacado" data-product-id="' + producto.id + '" style="border: 1px solid #e5e7eb; border-radius: 12px; overflow: hidden; max-width: 400px; background: white; margin: 0 auto; box-shadow: 0 10px 40px rgba(0,0,0,0.1);">' +
            imagen +
            '<div style="padding: 24px;">' +
                '<div style="display: inline-block; padding: 4px 12px; background: #f59e0b; color: white; border-radius: 20px; font-size: 12px; font-weight: 600; margin-bottom: 12px;">DESTACADO</div>' +
                '<div style="font-size: 22px; font-weight: 700; color: #1f2937; margin-bottom: 12px;">' + producto.nombre + '</div>' +
                '<div style="margin-bottom: 16px;">' + precioHtml + '</div>' +
                '<button class="tienda-agregar-btn" data-product-id="' + producto.id + '" style="width: 100%; padding: 14px; background: #3b82f6; color: white; border: none; border-radius: 8px; font-weight: 600; cursor: pointer;">Agregar al Carrito</button>' +
            '</div>' +
        '</div>';
    }}

    function showAuthModal() {{
        var existing = document.getElementById('auth-modal-overlay');
        if (existing) return;

        var overlay = document.createElement('div');
        overlay.id = 'auth-modal-overlay';
        overlay.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.5);z-index:9999;display:flex;align-items:center;justify-content:center;';
        overlay.innerHTML = '<div style="background:white;padding:40px;border-radius:12px;max-width:400px;width:90%;text-align:center;">' +
            '<h2 style="margin:0 0 20px;color:#1f2937;">Iniciar Sesión</h2>' +
            '<p style="color:#6b7280;margin-bottom:20px;">Debes iniciar sesión para usar el carrito</p>' +
            '<button onclick="document.getElementById(\\'auth-modal-overlay\\').remove()" style="padding:10px 20px;background:#6b7280;color:white;border:none;border-radius:6px;cursor:pointer;margin-right:10px;">Cerrar</button>' +
        '</div>';
        document.body.appendChild(overlay);
    }}

    function buildMiniCarritoPopup(carrito, productos) {{
        var itemsHtml = '';
        var total = 0;

        if (!carrito || !carrito.items || carrito.items.length === 0) {{
            itemsHtml = '<div style="text-align:center;color:#6b7280;padding:20px;">Tu carrito está vacío</div>';
        }} else {{
            carrito.items.forEach(function(item) {{
                var producto = null;
                if (item.producto) producto = item.producto;
                else if (productos) {{ productos.forEach(function(p) {{ if (p.id === item.producto_id) producto = p; }}); }}

                var nombre = producto ? producto.nombre : 'Producto';
                var precio = producto ? parseFloat(producto.precio) : 0;
                var itemTotal = precio * item.cantidad;
                total += itemTotal;

                itemsHtml += '<div style="display:flex;justify-content:space-between;align-items:center;padding:12px 0;border-bottom:1px solid #e5e7eb;">' +
                    '<div style="flex:1;"><div style="font-weight:500;color:#1f2937;">' + nombre + '</div><div style="font-size:13px;color:#6b7280;">' + item.cantidad + ' x S/ ' + precio.toFixed(2) + '</div></div>' +
                    '<div style="font-weight:600;color:#1f2937;">S/ ' + itemTotal.toFixed(2) + '</div>' +
                '</div>';
            }});
        }}

        return '<div id="mini-carrito-popup" style="position:fixed;top:0;right:0;width:380px;height:100%;background:white;box-shadow:-4px 0 20px rgba(0,0,0,0.15);z-index:9999;display:flex;flex-direction:column;">' +
            '<div style="padding:16px;border-bottom:1px solid #e5e7eb;display:flex;justify-content:space-between;align-items:center;">' +
                '<h3 style="margin:0;font-size:18px;color:#1f2937;">🛒 Carrito</h3>' +
                '<button id="mini-carrito-cerrar" style="background:none;border:none;font-size:24px;cursor:pointer;color:#6b7280;">×</button>' +
            '</div>' +
            '<div style="padding:16px;max-height:300px;overflow-y:auto;">' + itemsHtml + '</div>' +
            '<div style="padding:16px;border-top:1px solid #e5e7eb;">' +
                '<div style="display:flex;justify-content:space-between;margin-bottom:12px;font-size:18px;font-weight:700;">' +
                    '<span>Total:</span><span>S/ ' + total.toFixed(2) + '</span>' +
                '</div>' +
                '<button class="mini-carrito-checkout" style="width:100%;padding:14px;background:#10b981;color:white;border:none;border-radius:8px;font-size:16px;font-weight:600;cursor:pointer;">Proceder al Pago</button>' +
            '</div>' +
        '</div>';
    }}

    function openMiniCarrito() {{
        var existing = document.getElementById('mini-carrito-popup');
        if (existing) {{
            existing.remove();
        }}
        
        getCarrito().then(function(carrito) {{
            getProductos().then(function(productos) {{
                var popup = buildMiniCarritoPopup(carrito, productos);
                document.body.insertAdjacentHTML('beforeend', popup);
                
                document.getElementById('mini-carrito-cerrar').onclick = function() {{
                    document.getElementById('mini-carrito-popup').remove();
                }};
                
                var checkoutBtn = document.querySelector('.mini-carrito-checkout');
                if (checkoutBtn) {{
                    checkoutBtn.onclick = function() {{
                        var user = getUserData();
                        if (!user) {{
                            document.getElementById('mini-carrito-popup').remove();
                            showAuthModal();
                            return;
                        }}
                        
                        getCarrito().then(function(carrito) {{
                            if (!carrito || !carrito.items || carrito.items.length === 0) {{
                                alert('Tu carrito está vacío');
                                return;
                            }}
                            
                            var checkoutData = {{
                                nombre_cliente: user.first_name || user.name || '',
                                email_cliente: user.email || '',
                                telefono_cliente: user.phone || '',
                                metodo_pago: 'efectivo',
                                usuario_id: user.id
                            }};
                            
                            fetch(API + '/checkout', {{
                                method: 'POST',
                                headers: getAuthHeaders(),
                                body: JSON.stringify(checkoutData)
                            }})
                            .then(function(r) {{ 
                                if (!r.ok) return r.text().then(t => {{ throw new Error(t) }});
                                return r.json(); 
                            }})
                            .then(function(data) {{
                                if (data.pedido) {{
                                    alert('¡Pedido realizado! Código: ' + data.pedido.codigo);
                                    document.getElementById('mini-carrito-popup').remove();
                                    window.location.reload();
                                }} else if (data.detail) {{
                                    alert(data.detail);
                                }}
                            }})
                            .catch(e => alert("Error en el servidor: " + e.message));
                        }});
                    }};
                }}
            }});
        }});
    }}

    function updateMiniCarrito(carrito) {{
        var miniCarrito = document.querySelector('.tienda-mini-carrito');
        if (!miniCarrito) return;
        
        var count = 0;
        var total = 0;
        
        if (carrito && carrito.items) {{
            count = carrito.items.reduce(function(sum, item) {{ return sum + item.cantidad; }}, 0);
            total = parseFloat(carrito.total || 0);
        }}
        
        var contador = miniCarrito.querySelector('.carrito-contador');
        var totalSpan = miniCarrito.querySelector('.carrito-total');
        
        if (contador) contador.textContent = count;
        if (totalSpan) totalSpan.textContent = 'S/ ' + total.toFixed(2);
    }}

    function renderCarritoPage(carrito) {{
        var carritoSection = document.querySelector('.tienda-carrito-items');
        if (!carritoSection) return;

        var user = getUserData();
        
        var isSuccess = carritoSection.querySelector('h2') && carritoSection.querySelector('h2').textContent.includes('Realizada');
        if (isSuccess) return;

        if (!carrito || !carrito.items || carrito.items.length === 0) {{
            carritoSection.innerHTML = '<div style="text-align: center; color: #6b7280; padding: 40px;">Tu carrito está vacío</div>';
            var existingSummary = document.querySelector('.tienda-carrito-summary');
            if (existingSummary) existingSummary.remove();
            return;
        }}

        var itemsHtml = '';
        var subtotal = 0;

        carrito.items.forEach(function(item) {{
            var precio = parseFloat(item.producto ? item.producto.precio : 0) || 0;
            var cantidad = parseInt(item.cantidad || 1);
            var itemTotal = precio * cantidad;
            subtotal += itemTotal;

            var imagenHtml = '';
            if (item.producto && item.producto.imagenes && item.producto.imagenes.length > 0) {{
                imagenHtml = '<img src="' + item.producto.imagenes[0] + '" style="width: 80px; height: 80px; object-fit: cover; border-radius: 8px;">';
            }} else {{
                imagenHtml = '<div style="width: 80px; height: 80px; background: #f3f4f6; border-radius: 8px; display: flex; align-items: center; justify-content: center;">📦</div>';
            }}

            itemsHtml += '<div class="carrito-item" data-item-id="' + item.id + '" style="display: flex; gap: 16px; padding: 16px 0; border-bottom: 1px solid #e5e7eb; align-items: center;">' +
                imagenHtml +
                '<div style="flex: 1;">' +
                    '<div style="font-weight: 600; color: #1f2937; margin-bottom: 4px;">' + (item.producto ? item.producto.nombre : 'Producto') + '</div>' +
                    '<div style="color: #6b7280; font-size: 14px;">S/ ' + precio.toFixed(2) + ' x ' + cantidad + '</div>' +
                '</div>' +
                '<div style="text-align: right;">' +
                    '<div style="font-weight: 700; color: #1f2937;">S/ ' + itemTotal.toFixed(2) + '</div>' +
                    '<button class="carrito-eliminar-btn" data-item-id="' + item.id + '" style="margin-top: 8px; padding: 6px 12px; background: #ef4444; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 12px;">Eliminar</button>' +
                '</div>' +
            '</div>';
        }});

        var igv = subtotal * 0.18;
        var total = subtotal + igv;

        var summaryHtml = '<div style="background: white; border-radius: 12px; padding: 24px; margin-top: 24px;">' +
            '<h3 style="margin-bottom:15px; color:#1f2937;">Datos de Pedido</h3>' +
            '<div style="margin-bottom: 20px;">' +
                '<input type="text" id="chk-nombre" placeholder="Nombre" style="width:100%; padding:10px; margin-bottom:10px; border:1px solid #ddd; border-radius:6px;" value="' + (user ? (user.first_name || user.name || '') : '') + '">' +
                '<input type="email" id="chk-email" placeholder="Email" style="width:100%; padding:10px; margin-bottom:10px; border:1px solid #ddd; border-radius:6px;" value="' + (user ? (user.email || '') : '') + '">' +
                '<input type="text" id="chk-telefono" placeholder="Teléfono" style="width:100%; padding:10px; border:1px solid #ddd; border-radius:6px;" value="' + (user ? (user.phone || '') : '') + '">' +
            '</div>' +
            '<div style="display: flex; justify-content: space-between; margin-bottom: 12px; color: #4b5563;">' +
                '<span>Subtotal:</span>' +
                '<span>S/ ' + subtotal.toFixed(2) + '</span>' +
            '</div>' +
            '<div style="display: flex; justify-content: space-between; margin-bottom: 12px; color: #4b5563;">' +
                '<span>IGV (18%):</span>' +
                '<span>S/ ' + igv.toFixed(2) + '</span>' +
            '</div>' +
            '<div style="display: flex; justify-content: space-between; font-size: 20px; font-weight: 700; color: #1f2937; padding-top: 12px; border-top: 1px solid #e5e7eb;">' +
                '<span>Total:</span>' +
                '<span>S/ ' + total.toFixed(2) + '</span>' +
            '</div>' +
            '<button class="carrito-checkout-btn" style="width: 100%; margin-top: 20px; padding: 16px; background: #10b981; color: white; border: none; border-radius: 8px; font-size: 16px; font-weight: 600; cursor: pointer;">Proceder al Pago</button>' +
        '</div>';

        var existingSummary = document.querySelector('.tienda-carrito-summary');
        if (existingSummary) existingSummary.remove();

        carritoSection.innerHTML = itemsHtml;
        carritoSection.insertAdjacentHTML('afterend', '<div class="tienda-carrito-summary">' + summaryHtml + '</div>');

        document.querySelectorAll('.carrito-eliminar-btn').forEach(function(btn) {{
            btn.onclick = function() {{
                var itemId = this.getAttribute('data-item-id');
                fetch(API + '/carrito/items/' + itemId, {{
                    method: 'DELETE',
                    headers: getAuthHeaders()
                }})
                .then(function() {{
                    getCarrito().then(renderCarritoPage);
                }});
            }};
        }});

        var checkoutBtn = document.querySelector('.carrito-checkout-btn');
        if (checkoutBtn) {{
            checkoutBtn.onclick = function() {{
                var user = getUserData();
                if (!user) {{ showAuthModal(); return; }}

                var nameVal = document.getElementById('chk-nombre').value;
                var emailVal = document.getElementById('chk-email').value;
                var phoneVal = document.getElementById('chk-telefono').value;

                if (!nameVal || !emailVal) {{ alert("Nombre y Email son requeridos"); return; }}

                checkoutBtn.disabled = true;
                checkoutBtn.textContent = 'Procesando...';

                var checkoutData = {{
                    nombre_cliente: nameVal,
                    email_cliente: emailVal,
                    telefono_cliente: phoneVal,
                    metodo_pago: 'efectivo',
                    usuario_id: user.id
                }};

                fetch(API + '/checkout', {{
                    method: 'POST',
                    headers: getAuthHeaders(),
                    body: JSON.stringify(checkoutData)
                }})
                .then(function(r) {{ 
                    if (!r.ok) return r.text().then(t => {{ throw new Error(t) }});
                    return r.json(); 
                }})
                .then(function(data) {{
                    if (data.pedido) {{
                        var successHtml = '<div style="text-align: center; padding: 40px;">' +
                            '<div style="font-size: 60px; margin-bottom: 20px;">✅</div>' +
                            '<h2 style="color: #059669; margin-bottom: 10px;">¡Compra Realizada!</h2>' +
                            '<p style="color: #6b7280; margin-bottom: 20px;">Código: <b>' + data.pedido.codigo + '</b></p>' +
                            '<button onclick="window.location.reload()" style="margin-top: 20px; padding: 12px 24px; background: #3b82f6; color: white; border: none; border-radius: 8px; cursor: pointer;">Aceptar</button>' +
                        '</div>';
                        
                        var summary = document.querySelector('.tienda-carrito-summary');
                        if (summary) summary.remove();
                        carritoSection.innerHTML = successHtml;
                    }} else {{
                        alert(data.detail || "Error en el pedido");
                        checkoutBtn.disabled = false;
                        checkoutBtn.textContent = 'Proceder al Pago';
                    }}
                }})
                .catch(e => {{
                    alert("Error en el servidor: " + e.message);
                    checkoutBtn.disabled = false;
                    checkoutBtn.textContent = 'Proceder al Pago';
                }});
            }};
        }}
    }}

    function initCarrito() {{
        getCarrito().then(function(carrito) {{
            updateMiniCarrito(carrito);
            renderCarritoPage(carrito);
        }});

        document.querySelectorAll('.tienda-mini-carrito').forEach(function(carrito) {{
            carrito.onclick = openMiniCarrito;
        }});

        document.querySelectorAll('.tienda-agregar-btn').forEach(function(btn) {{
            btn.onclick = function() {{
                var user = getUserData();
                if (!user) {{ showAuthModal(); return; }}

                var productId = this.getAttribute('data-product-id');
                var btnText = this.textContent;
                this.disabled = true;
                this.textContent = '...';

                fetch(API + '/carrito/items', {{
                    method: 'POST',
                    headers: getAuthHeaders(),
                    body: JSON.stringify({{ producto_id: parseInt(productId), cantidad: 1, usuario_id: user.id }})
                }})
                .then(function(r) {{ return r.json(); }})
                .then(function() {{
                    getCarrito().then(function(c) {{
                        updateMiniCarrito(c);
                        renderCarritoPage(c);
                    }});
                }})
                .finally(function() {{
                    btn.disabled = false;
                    btn.textContent = btnText;
                }});
            }};
        }});
    }}

    var carouselRendered = false;

    function replaceCards() {{
        getProductos().then(function(productos) {{
            if (productos.length === 0) return;

            var cards = document.querySelectorAll('.tienda-producto-card');
            cards.forEach(function(card, index) {{
                var producto = productos[index % productos.length];
                if (producto) card.outerHTML = buildCard(producto);
            }});

            var grilla = document.querySelector('.tienda-productos-grid');
            if (grilla) {{
                var placeholder = grilla.querySelector('div');
                if (placeholder && placeholder.textContent.indexOf('aparecerán') !== -1) {{
                    placeholder.outerHTML = buildGrilla(productos);
                }}
            }}

            var destacado = document.querySelector('[data-gjs-type="tienda-producto-destacado"]');
            if (destacado && productos.length > 0) {{
                destacado.outerHTML = buildDestacado(productos[0]);
            }}
        }}).finally(function() {{
            if (!carouselRendered) {{
                carouselRendered = true;
                initCarrito();
            }}
        }});
    }}

    if (document.readyState === 'loading') {{
        document.addEventListener('DOMContentLoaded', replaceCards);
    }} else {{
        replaceCards();
    }}
}})();
</script>'''
    return script