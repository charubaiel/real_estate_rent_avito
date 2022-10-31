FROM python:3.8-slim

ENV DAGSTER_HOME=/opt/dagster/dagster_home/
ENV DAGSTER_PORT=3000
ENV POETRY_VIRTUALENVS_CREATE=False

RUN mkdir -p /opt/dagster/dagster_home /opt/dagster/app
RUN touch /opt/dagster/dagster_home/dagster.yaml 

WORKDIR /opt/dagster/app

COPY . /opt/dagster/app/

RUN apt-get update

RUN pip install poetry && apt-get install -y --no-install-recommends firefox-esr 

RUN poetry install --no-interaction --no-ansi

CMD ["/bin/bash","-c","dagit -h 0.0.0.0 -p ${DAGSTER_PORT} & dagster-daemon run"]
