FROM python:3.8-slim-buster
LABEL author="Cristiano"

WORKDIR /app

USER root

COPY requirements.txt /app
COPY main.py /app

RUN pip3 install -r requirements.txt

CMD python main.py
