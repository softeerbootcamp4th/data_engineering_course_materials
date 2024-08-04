# notebook/Dockerfile
FROM jupyter/pyspark-notebook:latest

USER root

RUN apt-get update && apt-get install -y openjdk-8-jdk python3 python3-pip && apt-get clean

RUN ln -s /usr/bin/python3 /usr/bin/python

ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
ENV PATH=$PATH:$JAVA_HOME/bin

RUN pip3 install matplotlib pyspark pandas

COPY start-notebook.sh /start-notebook.sh

RUN chmod +x /start-notebook.sh

USER $NB_UID

CMD ["/bin/bash", "/start-notebook.sh"]
