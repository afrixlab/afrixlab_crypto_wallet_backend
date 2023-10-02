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

COPY --chown=django:django ./devops/celery/worker/start.sh /start-celeryworker.sh
RUN sed -i 's/\r$//g' /start-celeryworker.sh
RUN chmod +x /start-celeryworker.sh


COPY --chown=django:django ./devops/celery/beat/start.sh /start-celerybeat.sh
RUN sed -i 's/\r$//g' /start-celerybeat.sh
RUN chmod +x /start-celerybeat.sh


ADD requirements requirements
RUN pip install -r requirements/local.txt

ADD . .
EXPOSE 8008
CMD ["python", "manage.py", "runserver", "0.0.0.0:8008"]
