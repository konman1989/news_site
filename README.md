# News site
## Python 3.8, Django 3

This is a simple news site with different types of users - regular users, editors and administrators.
Users' posts need to be approved by admins first, where editors' and admins' don't.
## DB config
To use a prebuilt groups and permissions run:
```
pip install -r requirements.txt
```
python manage.py migrate
```
loaddata users.json groups.json
```

## ENV config
ENV config can be set up by:
```
cp .env-example .env
```
Make sure to set all required variables.

## Celery + Redis.
This app uses Celery + Redis as brokers to send emails. Make sure to set up Redis
on your machine and run:
```
redis-server
```
```
celery worker -A news
```
