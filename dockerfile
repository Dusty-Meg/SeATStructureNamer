FROM python:3.11.0rc2-slim

WORKDIR /app

RUN apt-get update

RUN apt-get install python3-dev default-libmysqlclient-dev gcc  -y

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY Run.py /app
COPY DAL.py /app
COPY ESI.py /app

CMD python -u Run.py