FROM python:3.8-slim

RUN mkdir -p /opt/dagster/dagster_home /opt/dagster/app

RUN pip install dagit dagster-postgres pandas requests lxml numpy bs4

# Copy your code and workspace to /opt/dagster/app
COPY . /opt/dagster/app

ENV DAGSTER_HOME=/opt/dagster/dagster_home/

# Copy dagster instance YAML to $DAGSTER_HOME
# COPY dagster.yaml /opt/dagster/dagster_home/

WORKDIR /opt/dagster/app

EXPOSE 80

ENTRYPOINT ["dagit", "-p", "80"]