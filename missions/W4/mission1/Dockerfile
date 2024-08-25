# Base image: Bitnami Spark with Hadoop
FROM bitnami/spark:3.2.0

# Install necessary packages
USER root
RUN install_packages \
    python3 \
    python3-pip \
    curl \
    wget

# Upgrade pip and install additional Python packages
RUN pip3 install --upgrade pip
RUN pip3 install jupyter requests selenium matplotlib pandas chromedriver-autoinstaller

# Set up working directory
WORKDIR /app

# Copy the notebook into the container
COPY analyze.ipynb /app/analyze.ipynb

# Install Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && dpkg -i google-chrome-stable_current_amd64.deb || apt-get -fy install \
    && apt-get clean \
    && rm google-chrome-stable_current_amd64.deb

# Create the /mnt/data directory for mounting
RUN mkdir -p /mnt/data

# Start Spark Master and Jupyter notebook
CMD ["/bin/bash", "-c", "/opt/bitnami/spark/bin/spark-class org.apache.spark.deploy.master.Master & jupyter notebook --ip=0.0.0.0 --allow-root --no-browser --NotebookApp.token='' --NotebookApp.password=''"]
