FROM python:3.10-slim

ARG PRIVAT_SSH
ARG PUBLIC_SSH

RUN apt-get update && apt-get install nano && apt-get install -y git
RUN git config --global user.email "aleksandrin.a@mail.ru" && git config --global user.name "Charubaiel"

ENV PROJECT_PATH /home/project/

COPY . /home/project/
WORKDIR /home/project/

RUN --mount=type=ssh mkdir -p -m 0600 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts 
RUN echo "$PRIVAT_SSH" > ~/.ssh/id_ed25519 && \
    echo "$PUBLIC_SSH" > ~/.ssh/id_ed25519.pub && \
    chmod 600 ~/.ssh/id_ed25519 && \
    chmod 600 ~/.ssh/id_ed25519.pub

RUN pip install --no-cache-dir -r req.txt

CMD ["/bin/bash","-c", "python parse.py && git add . && git commit -m 'update db' && git push -u git@github.com:charubaiel/real_estate_rent_avito.git test"]