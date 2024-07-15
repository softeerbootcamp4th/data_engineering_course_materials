#!/bin/bash

# 깃허브 레포지토리 동기화
if [ -d "/app/softeer/.git" ]; then
    cd /app/softeer && git pull
else
    git clone https://github.com/jang-namu/data-engineering-course.git /app/softeer
fi

jupyter lab --ip='*' --port=8889 --no-browser --allow-root --NotebookApp.token='' --NotebookApp.password=''