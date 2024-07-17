FROM python:3.10.14-slim AS build

# Set the working directory
WORKDIR /app
COPY . /app

# Install dependencies / Remove file
RUN apt-get update && apt-get install -y \
    fonts-nanum-coding \
    fonts-nanum-extra \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt
RUN rm -rf /app/requirements.txt
RUN cp /usr/share/fonts/truetype/nanum/Nanum* /usr/local/lib/python3.10/site-packages/matplotlib/mpl-data/fonts/ttf/ \
    && rm -rf /home/ubuntu/.cache/matplotlib/*

FROM python:3.10.14-slim 

# Set the working directory
WORKDIR /app

# Copy the dependencies
COPY --from=build /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=build /usr/local/bin /usr/local/bin
COPY --from=build /app /app
COPY --from=build /usr/local/share/jupyter /usr/local/share/jupyter
COPY --from=build /usr/share/fonts/truetype/nanum /usr/share/fonts/truetype/nanum

# Expose the port
EXPOSE 8888
EXPOSE 8501
EXPOSE 8123

# Run the application
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--allow-root", "--no-browser"]
