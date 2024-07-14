#!/bin/bash
FROM ubuntu:jammy

ENV INSTANCE_IP="0.0.0.0"

ENV NB_USER="nbuser"
ENV NB_UID="1000"
ENV NB_GID="100"


USER root

RUN apt update -y && \
    apt upgrade -y && \
    apt install -y python3 python-is-python3 python3-pip && \
    useradd --no-log-init --create-home --shell /bin/bash --uid "${NB_UID}" --no-user-group "${NB_USER}"

USER ${NB_UID}

WORKDIR /home/${NB_USER}
COPY ./*.ipynb /home/${NB_USER}/
COPY ./requirements.txt /home/${NB_USER}/
COPY ./mtcars.csv /home/${NB_USER}/
COPY ./start.sh /home/

USER root

WORKDIR /home/${NB_USER}
RUN chown ${NB_USER}:users /home/start.sh

USER ${NB_UID}

WORKDIR /home
RUN chmod 755 ./start.sh
ENV JUPYTER_PORT=8587
EXPOSE ${JUPYTER_PORT}

CMD ./start.sh ${NB_USER} ${JUPYTER_PORT} ${INSTANCE_IP}