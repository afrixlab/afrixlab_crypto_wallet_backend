FROM ubuntu:latest
FROM python:3.10
RUN apt-get -y update && apt-get install -y libmagic-dev

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /cryptowallet

RUN addgroup --system django \
    && adduser --system --ingroup django django


COPY --chown=django:django ./devops/start.sh /start.sh
RUN sed -i 's/\r$//g' /start.sh
RUN chmod +x /start.sh
ADD requirements requirements
RUN pip install -r requirements/local.txt

ADD . .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
