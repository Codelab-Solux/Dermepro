# /!/bin/bash
# Build the project
echo 'Building the project ../..'
python3.9 pip install -r requirements.txt

echo 'Collecting static files ../..'
python3.9 manage.py collectstatic --noinput --clear