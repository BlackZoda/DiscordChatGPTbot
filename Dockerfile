FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

COPY .env .env

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]