FROM python:3.12.3
WORKDIR /app

RUN useradd -m appuser

COPY apps/api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY apps/api/app ./app
COPY apps/api/tests ./tests
COPY apps/api/pytest.ini .
COPY packages ./packages
RUN chown -R appuser:appuser /app
USER appuser
ENV PYTHONPATH=/app:$PYTHONPATH

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--reload-delay", "0.5"]