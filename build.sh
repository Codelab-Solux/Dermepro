# /!/bin/bash
# Build the project
echo 'Building the project ../..'
pip install -r requirements.txt

echo 'Collecting static files ../..'
python3.9 manage.py collectstatic --noinput --clear

sudo docker build -t dermepro .
sudo docker run -d -p 8000:8000 dermepro
docker-compose up

