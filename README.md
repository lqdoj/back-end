# LQDOJ's back-end

## First time clone

### 1. Install all requirement packages:
In Windows:
```bash
python -m pip install -r dependencies.txt
```
In Ubuntu:
```bash
sudo python3 -m pip install -r dependencies.txt
```
### 2. Migrate db
Run:
```bash
sudo python3 manage.py migrate
```

## Usage
To create superuser account, run:
```bash
sudo python3 manage.py createsuperuser
```
To run in th development server:
```bash
sudo python3 manage.py runserver 0.0.0.0:8000
```

Make sure you can access the admin page at:
```url
localhost:8000/admin
```
