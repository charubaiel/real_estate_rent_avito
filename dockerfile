FROM python:3.8-slim


WORKDIR /opt/dagster/app
COPY . /opt/dagster/app

RUN apt-get update
RUN apt-get install libgomp1
RUN pip install poetry

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

CMD ["dagster", "api", "grpc", "-h", "0.0.0.0", "-p", "4000", "-f", "pipeline.py"]
