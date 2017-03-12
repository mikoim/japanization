FROM alpine:latest

RUN apk add --no-cache \
    ca-certificates g++ gcc libffi-dev libxml2-dev libxslt-dev musl-dev postgresql-dev python3 python3-dev
RUN pip3 install --upgrade pip

WORKDIR /srv

COPY requirements.txt /srv/requirements.txt
RUN pip3 install -r requirements.txt

COPY . /srv
RUN python3 manage.py collectstatic --no-input

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0","japanization.wsgi:application"]

EXPOSE 8000
