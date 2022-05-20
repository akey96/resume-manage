FROM python:3.9
RUN mkdir /service
WORKDIR /service
COPY . /service/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install gunicorn psycopg2-binary
WORKDIR /service/service/
RUN python manage.py migrate --run-syncdb && \
    python manage.py loaddata seeders/data.json
CMD gunicorn --bind 0.0.0.0:8000 service.wsgi
