FROM python:3.8-slim

RUN mkdir -p /opt/dagster/dagster_home /opt/dagster/app

RUN mkdir -p -m 0600 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts 
RUN echo "$PRIVAT_SSH" > ~/.ssh/id_rsa && \
    echo "$PUBLIC_SSH" > ~/.ssh/id_rsa.pub && \
    chmod 600 ~/.ssh/id_rsa && \
    chmod 600 ~/.ssh/id_rsa.pub

RUN pip install dagit dagster-postgres pandas requests lxml numpy bs4

ARG PRIVAT_SSH
ARG PUBLIC_SSH

RUN apt-get update && apt-get install nano && apt-get install -y git
RUN git config --global user.email "aleksandrin.a@mail.ru" \
	&& git config --global user.name "Oracle_Server"


# Copy your code and workspace to /opt/dagster/app
COPY . /opt/dagster/app

ENV DAGSTER_HOME=/opt/dagster/dagster_home/

# Copy dagster instance YAML to $DAGSTER_HOME
# COPY dagster.yaml /opt/dagster/dagster_home/

WORKDIR /opt/dagster/app


CMD ["/bin/bash","-c", "git switch dbd && git fetch && git pull --rebase && dagster job execute -f jobs/avito_dbd.py -c ops.yaml\
    && git add . && git commit -m 'update db' && git push -u git@github.com:charubaiel/real_estate_rent_avito.git dbd"]