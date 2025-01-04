FROM python:3.11-slim

WORKDIR /app

COPY data/data.csv data/data.csv
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY food_order_assistant .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]