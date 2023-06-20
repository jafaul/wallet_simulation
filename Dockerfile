FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app
STOPSIGNAL SIGTERM
EXPOSE 3000/tcp
CMD ["python3", "main.py"]
CMD ["uvicorn", "main:app", "--reload", "--host", "localhost", "--port", "3000"]