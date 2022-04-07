# task_tracker_BE
## Steps to start the project locally 
 * python manage.py makemigrations account
 * python manage.py migrate
 * python manage.py makemigrations tasks projects
 * python manage.py migrate
 * python manage.py create_permissions

## To run the porject
 * python manage.py runserver
## To create super user
 * python manage.py createsuperuser

## To clean db
 * python manage.py flush

## To reset all migrations
  * delete the .sqlite file
  * delete all migrations folder inside apps
