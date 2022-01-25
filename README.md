## General info
RESTful API made with Django Rest Framework


### Local Setup
Configure your environment.
Activate virtualenv: (venv - your virtual environment name).
```shell
source venv/bin/activate
```

Then copy env.example to .env file and set up environment variables.
Export CONFIG_NAME variable. For local setup it should be set to base.

To make and apply migrations run the following command:
```shell
python3 manage.py makemigrations
python3 manage.py migrate
```

To start server go to the project root and run:
```shell
python3 manage.py runserver
```
