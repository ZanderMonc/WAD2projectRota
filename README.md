# WAD2projectRota
Web app dev project 2022

Link to the project down below:

http://zandermonc.pythonanywhere.com/timetable/

sources used: 
https://www.huiwenteo.com/normal/2018/07/24/django-calendar.html

To run RotaCare from your machine
steps
1: Clone the repository to your machine 
2; In anaconda command prompt cd to the local repo path
3 Run: conda create --name RotaCare (or venv / similar virtual environment creation)
4 Run: conda activate RotaCare
5 Run: pip install -r requirements.txt
6 Run: python manage.py makemigrations 
7 Run: python manage.py migrate 
9 run: python population_script.py
10 Run: python manage.py migrate 
11 Run if not done before: python manage.py createsuperuser
12 Run: python manage.py runserver 


13: Navigate on Web browser to 
Localhost address:8000
Ie  127.0.0.1:8000
14: to view RotaCare, login with superuser details or create a new user in register.

If re-running with fresh database, delete sql database with python manage.py flush and run all commands from step 6. 
