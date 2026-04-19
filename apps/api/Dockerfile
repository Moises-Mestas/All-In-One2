FROM python:3.12.3-slim

# 1. Crear el usuario con un UID numérico específico (1001) para que Snyk valide la seguridad
RUN useradd -m -u 1001 appuser
WORKDIR /app

# 2. Copiar dependencias y ejecutarlas
COPY apps/api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Usar --chown con el UID numérico directamente en el COPY
COPY --chown=1001:1001 apps/api/app ./app
COPY --chown=1001:1001 apps/api/tests ./tests
COPY --chown=1001:1001 apps/api/pytest.ini .
COPY --chown=1001:1001 packages ./packages

# 4. FIX: Agregar HEALTHCHECK para validar que el contenedor está vivo
# Docker ejecutará esto cada 30s. Usa python para hacer un ping al puerto 8000.
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/')" || exit 1

# 5. Cambiar al usuario seguro usando su UID en lugar de su nombre
USER 1001
ENV PYTHONPATH=/app:$PYTHONPATH

EXPOSE 8000

# Quitar el "--reload" para producción
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]