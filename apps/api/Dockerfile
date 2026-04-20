# 1. FIX Snyk: Actualizamos a 3.12.8 para eliminar las 5 vulnerabilidades de la imagen base
FROM python:3.12.8-slim

# 2. Snyk prefiere que el WORKDIR se declare antes
WORKDIR /app

# 3. Creamos el usuario sin privilegios
RUN useradd -m appuser

# 4. Copiamos e instalamos dependencias como root temporal (Snyk lo permite en fase de build)
COPY apps/api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiamos el código asginando la propiedad al usuario seguro
COPY --chown=appuser:appuser apps/api/app ./app
COPY --chown=appuser:appuser apps/api/tests ./tests
COPY --chown=appuser:appuser apps/api/pytest.ini .
COPY --chown=appuser:appuser packages ./packages

# 6. HEALTHCHECK limpio
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/')"

# 7. FIX Snyk: Cambiamos al usuario por su nombre (no ID numérico) justo antes de exponer
USER appuser
ENV PYTHONPATH=/app:$PYTHONPATH

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]