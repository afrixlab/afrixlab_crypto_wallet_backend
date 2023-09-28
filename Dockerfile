FROM ubuntu:latest
FROM python:3.11.4-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /cryptowallet

COPY . .


RUN pip install -r requirements/local.txt


EXPOSE 8000

CMD [ "python","manage.py","runserver", "0.0.0.0:8000"]