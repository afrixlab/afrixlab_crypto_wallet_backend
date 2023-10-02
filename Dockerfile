FROM ubuntu:latest
FROM python:3.10
RUN apt-get -y update && apt-get install -y libmagic-dev

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /cryptowallet

COPY . .


RUN pip install -r requirements/base.txt

EXPOSE 8000
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
