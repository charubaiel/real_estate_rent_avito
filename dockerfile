FROM python:3.8-slim
# ARG PRIVAT_SSH
# ARG PUBLIC_SSH

RUN mkdir -p /opt/dagster/dagster_home /opt/dagster/app



# RUN apt-get update && apt-get install nano && apt-get install -y git
# RUN git config --global user.email "aleksandrin.a@mail.ru" \
# 	&& git config --global user.name "Oracle_Server"

RUN pip install dagit dagster-postgres pandas requests lxml numpy bs4

# RUN mkdir -p -m 0600 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts 
# RUN echo "$PRIVAT_SSH" > ~/.ssh/id_rsa && \
#     echo "$PUBLIC_SSH" > ~/.ssh/id_rsa.pub && \
#     chmod 600 ~/.ssh/id_rsa && \
#     chmod 600 ~/.ssh/id_rsa.pub

# Copy your code and workspace to /opt/dagster/app
COPY . /opt/dagster/app

ENV DAGSTER_HOME=/opt/dagster/dagster_home/

# Copy dagster instance YAML to $DAGSTER_HOME
RUN touch /opt/dagster/dagster_home/dagster.yaml

EXPOSE 3000

WORKDIR /opt/dagster/app

ENTRYPOINT ['dagit','-h','0.0.0.0','-p','3000']
# CMD ["/bin/bash","-c", "git switch dbd && git fetch && git pull --rebase && dagster job execute -f jobs/avito_dbd.py -c ops.yaml\
#     && git add . && git commit -m 'update db' && git push -u git@github.com:charubaiel/real_estate_rent_avito.git dbd"]