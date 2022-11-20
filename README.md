# resume-manager
Application to manage resumes from developers

# Install
```
- git clone https://github.com/akey96/resume-manage.git
- virtualenv --python=python3.10 env
- source env/bin/activate
- pip install -r requirements.txt
- cd service/
- python manage.py migrate --run-syncdb
- python manage.py loaddata seeders/data.json
- python manage.py runserver
```
