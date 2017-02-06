# japanization

日本語化情報コミュニティのアレ

## Getting started

```bash
git clone https://github.com/mikoim/japanization.git
cd japanization
pip3 install -r requirements.txt

# we currently don't supply migration files.
./manage.py makemigrations
./manage.py migrate

./manage.py createsuperuser

# set environment variable or edit settings.py
export STEAM_API_KEY=0123456789ABCDEF

./manage.py runserver
```
