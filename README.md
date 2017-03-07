# japanization

日本語化情報コミュニティのアレ

## Getting started

```bash
git clone https://github.com/mikoim/japanization.git
cd japanization
pip3 install -r requirements.txt

# set environment variable or edit settings.py
export STEAM_API_KEY=0123456789ABCDEF # Required
export SECRET_KEY=abracadabra.... # Optional but highly recommended in production environment
export DEBUG=1 # Optional
export DATABASE_URL=postgres://foo:bar@foo:5432/bar # Optional
export REDIS_URL=redis://localhost:6379/ # Optional

# apply all migrations
python3 manage.py migrate

# create superuser
python3 manage.py createsuperuser

# run development server
python3 manage.py runserver
```

## Special commands

### Import reviews from groups on Steam

```bash
python3 manage.py syncreviews GROUP_NAME
```
