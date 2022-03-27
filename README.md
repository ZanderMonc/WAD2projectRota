# WAD2projectRota
RotaCare - Web app dev project 2022

Link to the project down below: </br>

http://zandermonc.pythonanywhere.com/ </br>

Sources used: </br>
https://www.huiwenteo.com/normal/2018/07/24/django-calendar.html </br>
https://getbootstrap.com/ </br>
https://www.w3schools.com/ </br>
https://www.djangoproject.com/ </br>

To run RotaCare from your machine </br>
Steps: </br>
1. Clone the repository to your machine </br>
2. In anaconda command prompt cd to the local repo path </br>
3. Run: conda create --name RotaCare (or venv / similar virtual environment creation) </br>
4. Run: conda activate RotaCare </br>
5. Run: pip install -r requirements.txt </br>
6. Run: python manage.py makemigrations  </br>
7. Run: python manage.py migrate  </br>
9. Run: python population_script.py </br>
10. Run: python manage.py migrate  </br>
11. Run if not done before: python manage.py createsuperuser </br>
12. Run: python manage.py runserver </br>

13. Navigate on Web browser to </br>
    Localhost address:8000</br>
    Ie  127.0.0.1:8000 </br>
14. to view RotaCare, login with superuser details or create a new user in register. </br>

If re-running with fresh database, delete sql database with python manage.py flush and run all commands from step 6. 
