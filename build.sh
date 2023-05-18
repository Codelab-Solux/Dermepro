# /!/bin/bash
# Build the project
echo 'Building the project ../..'
pip install -r requirements.txt

echo 'Collecting static files ../..'
python3.9 manage.py collectstatic --noinput --clear