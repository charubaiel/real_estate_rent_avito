FROM python:3.10



COPY cron /etc/cron.d/cron

COPY . /home/project/

RUN apt-get update && apt-get -y install cron && pip install --no-cache-dir -r /home/project/req.txt


RUN touch /var/log/cron.log && crontab /etc/cron.d/cron



CMD ["/bin/bash", "-c", "cron && tail -f /var/log/cron.log"]
