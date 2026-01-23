FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src/import_dataset_MongoDB.py /app/src/
COPY ./data/healthcare_dataset.csv /app/data/