# japanization

日本語化情報コミュニティのアレ

## Getting started

```bash
git clone https://github.com/mikoim/japanization.git
cd japanization
pip3 install -r requirements.txt
python3 manage.py migrate
python3 manage.py createsuperuser

# set environment variable or edit settings.py
export STEAM_API_KEY=0123456789ABCDEF # Required
export DEBUG=1 # Optional
export REDIS_URL=redis://localhost:6379/ # Optional

python3 manage.py runserver
```

## Special commands

### Import reviews from groups on Steam

```bash
python3 manage.py syncreviews GROUP_NAME
```
