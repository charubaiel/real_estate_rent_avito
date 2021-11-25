FROM python:3.10



RUN apt-get update && apt-get install -y cron && apt-get install nano

ENV PROJECT_PATH /home/project/

COPY . /home/project/
WORKDIR /home/project/

RUN pip install --no-cache-dir -r req.txt

COPY cron /etc/cron.d/cron

RUN touch  /var/log/cron.log
RUN chmod 0744 /etc/cron.d/cron
RUN crontab /etc/cron.d/cron


CMD ["/bin/bash", "-c", "cron && tail -f /var/log/cron.log"]