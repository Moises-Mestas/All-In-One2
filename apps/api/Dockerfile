FROM python:3.12.8-slim-bookworm

# 1. Crear grupo y usuario con UID altos (10001) para evitar choques con el sistema host
RUN groupadd -g 10001 appgroup && useradd -u 10001 -g 10001 -m appuser

WORKDIR /app

# 2. Copiar e instalar dependencias directamente
COPY --chown=appuser:appgroup apps/api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copiar el código al usuario seguro
COPY --chown=appuser:appgroup apps/api/app ./app
COPY --chown=appuser:appgroup apps/api/tests ./tests
COPY --chown=appuser:appgroup apps/api/pytest.ini .
COPY --chown=appuser:appgroup packages ./packages

ENV PYTHONPATH=/app:$PYTHONPATH
EXPOSE 8000

# 4. Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/')"

# 5. FIX FINAL: Cambiamos al usuario seguro JUSTO ANTES de ejecutar el contenedor
USER appuser

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]