FROM python:3.11-slim

WORKDIR /app

RUN pip install pipenv

COPY data/data.csv data/data.csv
COPY ["Pipfile", "Pipfile.lock", "./"]

RUN pipenv install --deploy --ignore-pipfile --system

COPY food_order_assistant .

EXPOSE 5000

# Modify the CMD to use a shell script
COPY start.sh .
RUN chmod +x start.sh
CMD ["./start.sh"]