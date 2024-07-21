sudo apt-get -y install python3.10-ven
python3 -m venv sentiment_env
. ./sentiment_env/bin/activate
pip install afinn
cd ./sentiment_env/lib/python3.10/site-packages/
sudo apt-get install -y zip
zip -r sentiment_env.zip *
mv sentiment_env.zip  ~/