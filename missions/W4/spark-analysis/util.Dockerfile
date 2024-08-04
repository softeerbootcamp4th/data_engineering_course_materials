FROM jnamu/hadoop-cluster-node

RUN apt-get install -y vim && \
    pip3 install pandas pyarrow matplotlib jupyter && \
    pip3 install numpy==1.24.0


