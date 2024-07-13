# base image
FROM python:3.12-slim

# work directory
WORKDIR /app

# essential packages installation
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-jdk \
    curl \
    && rm -rf /var/lib/apt/lists/*

# JPype1 and konlpy installation
RUN pip install --no-cache-dir JPype1

# mecab-ko 설치
#RUN curl -s https://raw.githubusercontent.com/konlpy/konlpy/master/scripts/mecab.sh | bash

# copy requirements.txt, W1, W2
COPY requirements.txt .
COPY w2 w2
COPY w1 w1

# pip dependencies installation
RUN pip install --no-cache-dir -r requirements.txt

# copy jupyter_config.py
COPY jupyter_config.py /root/.jupyter/jupyter_notebook_config.py

# expose port
EXPOSE 8888

# command to run jupyter lab
CMD ["jupyter-lab", "--config=/root/.jupyter/jupyter_notebook_config.py", "--allow-root"]
