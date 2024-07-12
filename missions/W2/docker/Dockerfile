FROM python:3.12
RUN apt-get  -y update && \
    apt-get  -y upgrade python3 python3-pip
            
RUN python3 -m pip config set global.break-system-packages true
RUN pip3 install jupyter pandas numpy seaborn matplotlib  
    
RUN useradd -ms /bin/bash jupyter
USER jupyter
WORKDIR /home/jupyter 
EXPOSE 8888                                           

COPY resources /home/jupyter
ENTRYPOINT ["jupyter", "notebook","--allow-root","--ip=0.0.0.0","--port=8888","--no-browser"]