FROM python:3.6-slim-buster

RUN apt-get update && \
    apt-get -y install sudo

ENV user dibyasom

RUN useradd -m -d /home/${user} ${user} && \
    chown -R ${user} /home/${user} && \
    adduser ${user} sudo && \
    echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

WORKDIR  /home/${user}/streamer

USER ${user}

COPY --chown=${user}:${user} requirements.txt .

RUN sudo apt-get update && \
    sudo apt-get install apt-utils tzdata -y && \
    sudo apt autoremove && \
    sudo mkdir {assets,workspace} && \
    export PATH="/home/${user}/.local/bin:$PATH" && \  
    pip install --no-cache-dir -r requirements.txt 

ENV GOOGLE_APPLICATION_CREDENTIALS="/home/dibyasom/streamer/assets/creds.json" TZ="Asia/Kolkota"

WORKDIR /home/${user}/streamer/workspace

COPY --chown=${user} src/ .

CMD [ "python", "-m", "celery", "-A", "gcs_util", "worker", "--loglevel=INFO" ]