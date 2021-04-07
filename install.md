pip3 install pipenv 
pipenv install --three python-telegram-bot flask gunicorn requests
download ngrok
set token
pipenv install --three BeautifulSoup4
pipenv install --three redis

shell: pipenv run python3

pipenv lock -r > requirements.txt

# for firebase app
pipenv install --three pyrebase
