FROM python:3.12.3-slim

# 1. Crear el usuario y establecer el directorio de trabajo
RUN useradd -m appuser
WORKDIR /app

# 2. Copiar dependencias y ejecutarlas
COPY apps/api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. FIX: Usar --chown directamente en el COPY (Evita duplicar capas)
COPY --chown=appuser:appuser apps/api/app ./app
COPY --chown=appuser:appuser apps/api/tests ./tests
COPY --chown=appuser:appuser apps/api/pytest.ini .
COPY --chown=appuser:appuser packages ./packages

# Cambiar al usuario seguro
USER appuser
ENV PYTHONPATH=/app:$PYTHONPATH

EXPOSE 8000

# 4. FIX: Quitar el "--reload" para producción
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]