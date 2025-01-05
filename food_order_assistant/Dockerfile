FROM python:3.11-slim

WORKDIR /app

COPY data/data.csv data/data.csv
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the working directory
COPY src/ .

COPY .env .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]