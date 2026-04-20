# 1. FIX Snyk: Usamos bookworm que es la distribución de Linux más parcheada actualmente
FROM python:3.12.8-slim-bookworm

# 2. FIX Snyk: Crear grupo y usuario explícitamente por seguridad
RUN groupadd -r appgroup && useradd -r -g appgroup -m appuser

WORKDIR /app

# 3. FIX Snyk: Actualizar pip a la última versión para evitar alertas de "Unpinned package manager"
RUN pip install --no-cache-dir --upgrade pip

# 4. FIX Snyk: Cambiar al usuario seguro ANTES de instalar dependencias (Evita alerta de Root Privileges)
USER appuser

# 5. Agregar la carpeta bin del usuario al PATH para que reconozca uvicorn
ENV PATH="/home/appuser/.local/bin:${PATH}"

# 6. Copiar requirements asignando la propiedad al usuario y su grupo
COPY --chown=appuser:appgroup apps/api/requirements.txt .

# 7. Instalar dependencias usando el flag "--user" para que se instalen en la carpeta de appuser
RUN pip install --user --no-cache-dir -r requirements.txt

# 8. Copiar el resto del código
COPY --chown=appuser:appgroup apps/api/app ./app
COPY --chown=appuser:appgroup apps/api/tests ./tests
COPY --chown=appuser:appgroup apps/api/pytest.ini .
COPY --chown=appuser:appgroup packages ./packages

# 9. Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/')"

ENV PYTHONPATH=/app:$PYTHONPATH
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]