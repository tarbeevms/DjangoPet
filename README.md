# Template DjangoPet

To run this application:

Create an .env file with .env.example keys from the config directory and fill them with the necessary values.

Install dependencies: 
```python
poetry install
```

Activate the virtual environment: 
```python
poetry shell
```

Roll out migrations: 
```python
poetry run python manage.py migrate
```

Create a superuser to access the admin panel:
```python
poetry run python manage.py createsuperuser
```

Application launch: 
```python
poetry run python manage.py runserver
```
Admin panel:
http://127.0.0.1:8000/admin/
