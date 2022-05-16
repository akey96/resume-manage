# resume-manager
Application to manage resumes from developers

# Install
```
- git clone https://github.com/akey96/resume-manager.git
- pip install -r requirements.txt
- cd service/
- python manage.py migrate --run-syncdb
- python manage.py loaddata seeders/data.json
- python manage.py runserver
```