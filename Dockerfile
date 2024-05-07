FROM python:latest

RUN pip install pandas sqlalchemy psycopg2

WORKDIR /app 
COPY ingest_data.py ingest_data.py

ENTRYPOINT [ "python", "ingest_data.py" ]
