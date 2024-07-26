#!/bin/bash

docker cp pi.py spark-master:/opt/spark/bin/pi.py
docker exec -it spark-master sudo chown sparkuser:sparkuser /opt/spark/bin/pi.py
docker exec -it spark-master sudo chmod +x /opt/spark/bin/pi.py
docker exec -it spark-master /opt/spark/bin/spark-submit \
  --master spark://spark-master:7077 \
  /opt/spark/bin/pi.py