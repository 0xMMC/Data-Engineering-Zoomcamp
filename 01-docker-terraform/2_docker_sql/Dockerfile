FROM python:3.9.1

RUN apt-get install wget
RUN pip install pandas sqlalchemy psycopg2

WORKDIR /app
COPY my_ingest_data.py my_ingest_data.py 

ENTRYPOINT [ "python", "my_ingest_data.py" ]