FROM python:3.12.8-slim-bookworm

# 1. FIX Snyk: Crear grupo y usuario con un ID numérico estricto (1001)
RUN groupadd -g 1001 appgroup && useradd -u 1001 -g 1001 -m appuser

WORKDIR /app

# 2. FIX Snyk: Cambiamos al usuario usando su ID NUMÉRICO. 
# Esto apaga instantáneamente la alerta de "Root Privileges"
USER 1001

# 3. Configurar PATH
ENV PATH="/home/appuser/.local/bin:${PATH}"

# 4. Copiar requirements asignando la propiedad al ID 1001
COPY --chown=1001:1001 apps/api/requirements.txt .

# 5. FIX Snyk: Borramos el "upgrade pip" para evitar el "Unpinned package manager".
# Instalamos directamente los requirements.
RUN pip install --user --no-cache-dir -r requirements.txt

# 6. Copiar el resto del código
COPY --chown=1001:1001 apps/api/app ./app
COPY --chown=1001:1001 apps/api/tests ./tests
COPY --chown=1001:1001 apps/api/pytest.ini .
COPY --chown=1001:1001 packages ./packages

# 7. Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/')"

ENV PYTHONPATH=/app:$PYTHONPATH
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]