FROM spark_base

COPY worker_entrypoint.sh $SPARK_HOME/worker_entrypoint.sh
RUN chmod +x $SPARK_HOME/worker_entrypoint.sh

# RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
#     sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

EXPOSE 8081

CMD $SPARK_HOME/worker_entrypoint.sh
