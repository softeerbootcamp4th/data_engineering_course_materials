pip install -r /home/$1/requirements.txt 
python -m notebook --no-browser --port=$2 --NotebookApp.notebook_dir=/home/$1 --NotebookApp.ip=$3