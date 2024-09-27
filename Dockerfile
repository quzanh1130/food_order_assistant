FROM python:3.11-slim

WORKDIR /app

RUN pip install pipenv

COPY data/data.csv data/data.csv
COPY ["Pipfile", "Pipfile.lock", "./"]

RUN pipenv install --deploy --ignore-pipfile --system

COPY food_order_assistant .

EXPOSE 5000

CMD gunicorn --bind 0.0.0.0:5000 app:app