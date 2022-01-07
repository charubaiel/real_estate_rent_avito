FROM python:3.10-slim



RUN apt-get update && apt-get install nano && apt-get install -y git
RUN git config --global user.email "aleksandrin.a@mail.ru" && git config --global user.name "Charubaiel"

ENV PROJECT_PATH /home/project/

COPY . /home/project/
WORKDIR /home/project/

RUN --mount=type=ssh mkdir -p -m 0600 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts 
RUN pip install --no-cache-dir -r req.txt

CMD ["/bin/bash"]