# Use the official base image for Python
FROM --platform=amd64 python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file into the /app directory
COPY requirements.txt .

# Install the dependencies from requirements.txt
RUN pip install -r requirements.txt

RUN apt-get update
RUN apt-get upgrade -y 
RUN apt-get install git -y

# Expose port 8888 for JupyterLab
EXPOSE 8888

COPY start.sh .
RUN chmod +x start.sh

CMD ["./start.sh"]
