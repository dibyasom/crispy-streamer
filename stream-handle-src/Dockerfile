FROM python:3.6-slim-buster

RUN apt-get update && \
    apt-get -y install sudo

ENV user dibyasom

RUN useradd -m -d /home/${user} ${user} && \
    chown -R ${user} /home/${user} && \
    adduser ${user} sudo && \
    echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

WORKDIR  /home/${user}/shredder

USER ${user}

COPY --chown=${user}:${user} requirements.txt .

RUN sudo apt-get update && \
    sudo apt-get install apt-utils ffmpeg libsm6 libxext6 tzdata -y && \
    sudo apt autoremove && \
    sudo mkdir {assets,workspace} && \
    export PATH="/home/${user}/.local/bin:$PATH" && \     
    sudo pip install --no-cache-dir -r requirements.txt 

ENV TZ="Asia/Kolkota"

WORKDIR /home/${user}/shredder/workspace

CMD ["sudo", "python", "main.py" ]