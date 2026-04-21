FROM python:3.11-alpine

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["gunicorn", "Tienda.wsgi:application", "--bind", "0.0.0.0:8000"]