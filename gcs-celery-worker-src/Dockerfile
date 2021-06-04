FROM python:3.6-slim-buster

WORKDIR  /build

RUN apt-get update && \
    apt-get -y install sudo

ENV user dibyasom

RUN useradd -m -d /home/${user} ${user} && \
    chown -R ${user} /home/${user} && \
    adduser ${user} sudo && \
    echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER ${user}

RUN sudo apt-get update && \
    sudo apt-get install apt-utils tzdata -y && \
    sudo apt autoremove && \
    sudo mkdir assets && \
    sudo mkdir workspace

COPY requirements.txt .

RUN sudo pip install --no-cache-dir -r requirements.txt 

ENV GOOGLE_APPLICATION_CREDENTIALS="/build/secret/creds.json"

ENV TZ Asia/Kolkota

COPY --chown=${user} src/ workspace/

# COPY --chown=${user} creds.json assets/

WORKDIR /build/workspace

CMD [ "celery", "-A", "gcs_util", "worker", "--loglevel=INFO" ]