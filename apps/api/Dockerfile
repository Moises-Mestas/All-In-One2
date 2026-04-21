FROM python:3.12.8-slim-bookworm

# 1. Crear grupo y usuario con UID numérico alto (10001)
RUN groupadd -g 10001 appgroup && useradd -u 10001 -g 10001 -m appuser

WORKDIR /app

# 2. Cambiamos al usuario ID ANTES de hacer el pip install (Aprobado por Snyk)
USER 10001

# 3. Agregamos la carpeta local al PATH
ENV PATH="/home/appuser/.local/bin:${PATH}"
ENV PYTHONPATH=/app:$PYTHONPATH

# 4. Copiamos el requirements
COPY --chown=10001:10001 apps/api/requirements.txt .

# 5. FIX PEP-668: Agregamos --break-system-packages para permitir a pip instalar en Debian 12
RUN pip install --user --no-cache-dir --break-system-packages -r requirements.txt

# 6. Copiamos el resto del código
COPY --chown=10001:10001 apps/api/app ./app
COPY --chown=10001:10001 apps/api/tests ./tests
COPY --chown=10001:10001 apps/api/pytest.ini .
COPY --chown=10001:10001 packages ./packages

EXPOSE 8000

# 7. Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/')"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]