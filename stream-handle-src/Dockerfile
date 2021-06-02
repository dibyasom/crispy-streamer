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
    sudo apt-get install apt-utils ffmpeg libsm6 libxext6 tzdata -y && \
    echo 'export PATH="/home/dibyasom/.local/bin:$PATH"' > ~/.bashrc && \
    sudo apt autoremove && \
    sudo mkdir workspace && \
    sudo mkdir assets

COPY requirements.txt ./

RUN sudo pip install --no-cache-dir -r requirements.txt 

ENV GOOGLE_APPLICATION_CREDENTIALS="/build/secret/creds.json"

ENV TZ Asia/Kolkota

COPY --chown=dibyasom ./src/ assets/

WORKDIR /build/workspace

CMD [ "sudo", "python", "main.py" ]