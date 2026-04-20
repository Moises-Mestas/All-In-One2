FROM python:3.12.3-slim

# 1. Crear el usuario seguro ANTES de hacer cualquier otra cosa
RUN useradd -m -u 1001 appuser
WORKDIR /app

# 2. FIX: Cambiar al usuario seguro INMEDIATAMENTE para que todo le pertenezca a él
USER 1001

# 3. Configurar el PATH para que el sistema reconozca los paquetes instalados por este usuario
ENV PATH="/home/appuser/.local/bin:${PATH}"
ENV PYTHONPATH=/app:$PYTHONPATH

# 4. FIX: Agregar --chown también al requirements.txt (Error de tu imagen 2)
COPY --chown=1001:1001 apps/api/requirements.txt .

# 5. FIX: Instalar dependencias con el flag "--user" para no usar root (Error de tu imagen 1)
RUN pip install --user --no-cache-dir -r requirements.txt

# 6. Copiar el resto del código
COPY --chown=1001:1001 apps/api/app ./app
COPY --chown=1001:1001 apps/api/tests ./tests
COPY --chown=1001:1001 apps/api/pytest.ini .
COPY --chown=1001:1001 packages ./packages

# 7. FIX: Quitar el "|| exit 1" porque Docker ya sabe detectar fallos automáticamente (Error de tu imagen 3)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/')"

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]