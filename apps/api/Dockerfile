FROM python:3.14.4-slim-bookworm

# 1. Crear grupo y usuario con UID numérico alto (10001)
RUN groupadd -g 10001 appgroup && useradd -u 10001 -g 10001 -m appuser

WORKDIR /app

# 2. EL TRUCO MAESTRO: Cambiamos al usuario ID ANTES de hacer el pip install.
# Esto elimina la alerta de "Root privileges" al descargar paquetes de internet.
USER 10001

# 3. Al no ser root, pip instala en una carpeta local. Agregamos esa carpeta al PATH.
ENV PATH="/home/appuser/.local/bin:${PATH}"
ENV PYTHONPATH=/app:$PYTHONPATH

# 4. Copiamos el requirements asignando propiedad exclusiva al usuario 10001
COPY --chown=10001:10001 apps/api/requirements.txt .

# 5. FIX SNYK: Instalamos usando el flag "--user". Snyk valida que esto es 100% seguro.
RUN pip install --user --no-cache-dir -r requirements.txt

# 6. Copiamos el resto del código del sistema
COPY --chown=10001:10001 apps/api/app ./app
COPY --chown=10001:10001 apps/api/tests ./tests
COPY --chown=10001:10001 apps/api/pytest.ini .
COPY --chown=10001:10001 packages ./packages

EXPOSE 8000

# 7. Healthcheck para garantizar estabilidad del contenedor
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/')"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]